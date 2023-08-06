import copy
import os
import time
import threading
import pkg_resources

from ._mujocoviewer import MujocoViewer
from ._order import Order
from . import _pallet_visualizer

import mujoco
import pybullet
import mujoco_viewer
import pybullet_utils.bullet_client as bc
import cv2


# main class to run the simulation and preform the tests passed by the user this class is threadable and can run the
# simulation and the tests in different threads it supports 2 physics engines: mujoco and pybullet after loading
# using the load_order function, the user can run the simulation using the run_simulation function. additional
# functions are available to change the physics engine, the pallets and tests threads,
# and the callback function for images and loop callback
class Pallet_Sim:
    simulation_engines = ["mujoco", "pybullet"]

    class PyBulletProjectViewer:
        def __init__(self, data: tuple):
            self.__alive = True
            # make sure the data is a least 1 long and that the first element is a list and it was not more than 3 elements
            # if it has 1 or 2 elements, fill the rest with None (until 3 elements)
            if len(data) == 0:
                raise ValueError("data must have at least 1 element")
            if not isinstance(data[0], list):
                raise ValueError("The data must be a list of lists")
            if len(data) > 3:
                raise ValueError("The data must be a list of lists with a maximum of 3 elements")
            self.__view_thread = threading.Thread(target=self.__view_loop, args=data, daemon=True)
            self.__view_thread.start()

        def __view_loop(self, project_elements: list, texture_path: str = None,
                        shift: list[float, float, float] = None):
            def create_pybullet_element(physics_client_to_create: bc.BulletClient, element_dict: dict) -> int:
                el_id = physics_client_to_create.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                                      halfExtents=element_dict["halfExtents"])
                el_id = physics_client_to_create.createMultiBody(baseCollisionShapeIndex=el_id,
                                                                 basePosition=element_dict["basePosition"],
                                                                 baseMass=element_dict["baseMass"])
                return el_id

            physicsClient = bc.BulletClient(connection_mode=pybullet.GUI)
            physicsClient.setRealTimeSimulation(1)
            physicsClient.setGravity(0, 0, -10)
            physicsClient.createMultiBody(physicsClient.createCollisionShape(pybullet.GEOM_PLANE), 0)
            link_Masses = [25]

            if texture_path is not None and shift is not None:
                linkCollisionShapeIndices = [
                    physicsClient.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                       halfExtents=project_elements[0]["halfExtents"])]
                linkVisualShapeIndices = [physicsClient.createVisualShape(shapeType=pybullet.GEOM_MESH,
                                                                          fileName=texture_path,
                                                                          rgbaColor=[0.5, 0.3, 0.1, 1],
                                                                          visualFramePosition=shift)]
            else:
                linkCollisionShapeIndices = [
                    physicsClient.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                       halfExtents=project_elements[0]["halfExtents"])]
                linkVisualShapeIndices = [-1]
                print("Warning: Texture not found for product code: " + project_elements[0][
                    "product_code"] + " in specified texture dirs and subdirs")

            linkPositions = [project_elements[0]["halfExtents"]]
            linkOrientations = [[0, 0, 0, 1]]
            linkInertialFramePositions = [[0, 0, 0]]
            linkInertialFrameOrientations = [[0, 0, 0, 1]]
            indices = [0]
            jointTypes = [pybullet.JOINT_PRISMATIC]
            axis = [[1, 0, 0]]

            pallet_id = physicsClient.createMultiBody(baseMass=0,
                                                      linkMasses=link_Masses,
                                                      linkCollisionShapeIndices=linkCollisionShapeIndices,
                                                      linkVisualShapeIndices=linkVisualShapeIndices,
                                                      linkPositions=linkPositions,
                                                      linkOrientations=linkOrientations,
                                                      linkInertialFramePositions=linkInertialFramePositions,
                                                      linkInertialFrameOrientations=linkInertialFrameOrientations,
                                                      linkParentIndices=indices,
                                                      linkJointTypes=jointTypes,
                                                      linkJointAxis=axis)

            elements = []
            for element in project_elements[1:]:
                elements.append(create_pybullet_element(physicsClient, element))

            basePos = list(physicsClient.getBasePositionAndOrientation(pallet_id)[0])
            cameraPitch = -10
            cameraYaw = 140
            physicsClient.resetDebugVisualizerCamera(cameraDistance=3.5, cameraYaw=cameraYaw,
                                                     cameraPitch=cameraPitch,
                                                     cameraTargetPosition=basePos)

            while self.__alive:
                time.sleep(1)
            try:
                physicsClient.disconnect()
            except pybullet.error:
                pass

        def close(self):
            if self.__alive:
                self.__alive = False
                self.__view_thread.join()

    class MujocoProjectViewer:
        def __init__(self, data: tuple):
            self.__alive = True
            if len(data) == 1:
                data = (data[0], dict())
            elif len(data) > 2 or len(data) < 1:
                raise ValueError("Invalid data, expected tuple of length 1 or 2")
            self.__view_thread = threading.Thread(target=self.__view_loop, args=data, daemon=True)
            self.__view_thread.start()

        def __view_loop(self, raw_model: str, assets: dict):
            model = mujoco.MjModel.from_xml_string(raw_model, assets=assets)
            data = mujoco.MjData(model)

            # create the viewer object
            viewer = mujoco_viewer.MujocoViewer(model, data, height=800, width=800, title="Mujoco Viewer",
                                                hide_menus=True)

            # simulate and render
            while self.__alive:
                if viewer.is_alive:
                    mujoco.mj_step(model, data)
                    viewer.render()
                else:
                    break

            # close
            viewer.close()

        def close(self):
            self.__alive = False
            self.__view_thread.join()

    def __init__(self, *, tests=None, img_callback=None, loop_callback=None, texture_paths: list | str = None) -> None:
        if texture_paths is str:
            texture_paths = [texture_paths]
        if texture_paths is None:
            if os.path.isdir(pkg_resources.resource_filename(__name__, "./textures")):
                texture_paths = [pkg_resources.resource_filename(__name__, "./textures")]
            else:
                texture_paths = []

        self.__assets = dict()
        self.__texture_paths = []
        # load the assets if texture_dirs is a file path load it and if it's a directory load all the .stl and png files
        # raise if the file is not found or if folder is not found
        # load the assets by the file name with extension as the key
        for texture in texture_paths:
            if os.path.isfile(texture) and texture.endswith(".stl"):  # or texture.endswith(".png")):
                self.__assets[os.path.basename(texture).lower()] = open(texture, "rb").read()
                # append the full path to the texture
                self.__texture_paths.append(texture)
            elif os.path.isdir(texture):
                for file in os.listdir(texture):
                    if file.endswith(".stl"):  # or file.endswith(".png"):
                        self.__assets[file.lower()] = open(os.path.join(texture, file), "rb").read()
                        # append the full path to the texture
                        self.__texture_paths.append(os.path.join(texture, file))
            else:
                raise Exception("Texture not found")

        self.set_image_callback(img_callback)
        self.set_loop_callback(loop_callback)

        if tests is None:
            def create_step(test_time: float, force_x: float, force_y: float, period: float = 0.1) -> dict:
                return {
                    "time": test_time,
                    "force_x": force_x,
                    "force_y": force_y,
                    "period": period,
                }

            self.tests = [
                {
                    "name": "Still",
                    "duration": 30,
                    "steps": [
                        create_step(0, 0, 0)
                    ]
                },
                {
                    "name": "X axis",
                    "duration": 50,
                    "steps": [
                        create_step(5, 0.35, 0),
                        create_step(15, -0.35, 0)
                    ]
                },
                {
                    "name": "Y axis",
                    "duration": 50,
                    "steps": [
                        create_step(5, 0, 0.35),
                        create_step(15, 0, -0.35)
                    ]
                }
            ]
        else:
            self.tests = tests

        self.__order: Order | None = None
        self.__order_images = {
            "pallets": [],
            "width": 0,
            "height": 0
        }

    def __len__(self):
        return -1 if self.__order is None else len(self.__order)

    def set_image_callback(self, callback) -> None:
        if not (callable(callback) or callback is None):
            raise Exception("callback must be a function or None")
        self.__img_callback = callback

    def set_loop_callback(self, callback) -> None:
        if not (callable(callback) or callback is None):
            raise Exception("callback must be a function or None")
        self.__loop_callback = callback

    # get the pallets ids
    def get_pallet_nrs(self) -> list:
        return copy.deepcopy(self.__order.get_pallet_nrs())

    def get_pallet_nr(self, pallet_index: int) -> str:
        return self.__order.get_pallet_nr(pallet_index)

    def get_order_id(self) -> str:
        return self.__order.get_id()

    def get_order_images(self) -> dict:
        if self.__order is not None and len(self.__order_images["pallets"]) != len(self.__order):
            try:
                self.__order_images = self.__render_pallets()
            except Exception as e:
                if threading.current_thread() is not threading.main_thread():
                    raise Exception("Can't render pallets in a thread different than the main thread")
                else:
                    raise e
        return self.__order_images

    def get_assets(self) -> dict:
        return copy.deepcopy(self.__assets)

    def get_texture_paths(self) -> list:
        return copy.deepcopy(self.__texture_paths)

    def show_3D_pallet(self, pallet_index: int) -> None:
        if self.__order is not None and (pallet_index < 0 or pallet_index >= len(self.__order)):
            raise Exception("Pallet index out of range")
        if self.__order is None:
            raise Exception("No order loaded")
        _pallet_visualizer.show_pallet(self.__order.get_pallet(pallet_index), True)

    def show_all_3D_pallets(self) -> None:
        if self.__order is None:
            raise Exception("No order loaded")
        for i in range(len(self.__order)):
            self.show_3D_pallet(i)

    def show_2D_pallet(self, pallet_index: int) -> None:
        if pallet_index < 0 or pallet_index >= len(self.__order):
            raise Exception("Pallet index out of range")
        img = self.get_order_images()["pallets"][pallet_index]["images"]["product_code"]
        # display the image in a cv2 window and wait for a key press
        cv2.imshow("Pallet " + str(pallet_index), img)
        cv2.waitKey(0)

    # method for adding the order that will be simulated
    # use the json_data or path_data to load the order
    def load(self, *, json_data: str | dict = None, path_data: str = None) -> bool:
        self.__order = None
        self.__order_images = {
            "pallets": [],
            "width": 0,
            "height": 0
        }
        try:
            self.__order = Order(json_data=json_data, path_data=path_data)
        except Exception as e:
            print("Error loading order: " + str(e))
            self.__order = None
            return False
        return True

    def __render_pallets(self) -> dict:
        self.__order_images = {
            "pallets": [],
            "width": 0,
            "height": 0
        }
        viewer = MujocoViewer(width=300, height=600)
        width, height = viewer.get_dimensions()

        pallets_images = {
            "pallets": [],
            "width": width,
            "height": height
        }
        for i in range(len(self.__order)):
            pallets_images["pallets"].append({
                "images": {},
                "palletNr": self.__order.get_pallet_nrs()[i],
                "boxes": 0,
                "index": i
            })
            for color_by in ["product_code", "shipping_group", "weight"]:
                model = mujoco.MjModel.from_xml_string(
                    self.__order.get_model_data(model_type="mujoco", pallet_index=i, color_by=color_by), self.__assets)
                data = mujoco.MjData(model)
                pallets_images["pallets"][i]["boxes"] = model.nbody - 3
                # create the viewer object
                viewer.change_model(model)
                # simulate and render
                mujoco.mj_step(model, data)
                pallets_images["pallets"][i]["images"][color_by] = viewer.read_pixels(data)
        viewer.close()
        return pallets_images

    def export_pallet(self, pallet_index: int, simulation_type: str = "mujoco") -> tuple:
        if simulation_type not in ["mujoco", "pybullet"]:
            raise Exception("Simulation type not supported")
        if simulation_type == "mujoco":
            return self.__order.get_model_data(model_type="mujoco", pallet_index=pallet_index), self.__assets
        if simulation_type == "pybullet":
            raw_data = self.__order.get_model_data(model_type="pybullet", pallet_index=pallet_index)
            texture_path = None
            shift = [0, 0, 0]
            for t in self.__texture_paths:
                if raw_data[0]["product_code"].lower() in t.lower():
                    texture_path = t
                    break
            try:
                px, py, pz = self.__order.get_position_from_name(raw_data[0]["product_code"].lower())
                x, y, z = [r * 2 for r in raw_data[0]["halfExtents"]]
                px = - (x - px) / 2
                py = - (y - py) / 2
                pz = - (z - pz) / 2
                shift = [px, py, pz]
            except KeyError:
                texture_path = None
            return raw_data, texture_path, shift

    def run_simulation(self, *, simulation_engine="mujoco", pallet_nr="all", view: bool = True,
                       thread_tests: bool = True, thread_pallets: bool = True, **kwargs) -> dict:
        """
        :param simulation_engine: simulation engine to use
        :param pallet_nr: the pallet to simulate, if "all" all the pallets will be simulated
        :param view: if True the simulation will be rendered in a window
        :param thread_tests: if True the tests will be run in parallel threads
        :param thread_pallets: if True the pallets will be simulated in parallel threads
        :param kwargs: the arguments to pass to the simulation engine (view, thread_pallets, thread_tests,
                       fps(only for mujoco), palletNrs, etc.)
        """
        if simulation_engine not in ["mujoco", "pybullet"]:
            raise Exception("Simulation engine not supported")

        if pallet_nr not in ["all"] + self.get_pallet_nrs():
            raise Exception("Pallet id not found")

        if view and threading.current_thread() is not threading.main_thread():
            print("Warning: view is not supported in threadable mode, view will be disabled")
            view = False
        if view and (thread_tests or thread_pallets):
            print("Warning: Threading can't be used with view, threading will be disabled")
            thread_tests = False
            thread_pallets = False

        if simulation_engine == "mujoco":
            return self.__run_mujoco_simulation(view=view,
                                                thread_pallets=thread_pallets,
                                                thread_tests=thread_tests,
                                                pallet_nr=pallet_nr,
                                                color_by=kwargs.get("color_by", "product_code"),
                                                fps=kwargs.get("fps", 60))
        else:
            return self.__run_pybullet_simulation(view=view,
                                                  pallet_nr=pallet_nr,
                                                  thread_pallets=thread_pallets,
                                                  thread_tests=thread_tests)

    @staticmethod
    def __create_pybullet_element(physics_client_to_create: bc.BulletClient, element_dict: dict) -> int:
        el_id = physics_client_to_create.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                              halfExtents=element_dict["halfExtents"])
        el_id = physics_client_to_create.createMultiBody(baseCollisionShapeIndex=el_id,
                                                         basePosition=element_dict["basePosition"],
                                                         baseMass=element_dict["baseMass"])
        return el_id

    def __run_pybullet_simulation(self, view: bool = False, pallet_nr: str = "all", thread_tests: bool = True,
                                  thread_pallets: bool = True) -> dict:
        def run_test(raw_elements: list, test_data: dict, pallet_nr_index: int, test_index_data: int) -> None:
            if view:
                physicsClient = bc.BulletClient(connection_mode=pybullet.GUI)
            else:
                physicsClient = bc.BulletClient(connection_mode=pybullet.DIRECT)

            physicsClient.setRealTimeSimulation(0)
            physicsClient.setGravity(0, 0, -10)

            plane_id = physicsClient.createMultiBody(physicsClient.createCollisionShape(pybullet.GEOM_PLANE), 0)
            link_Masses = [25]
            linkCollisionShapeIndices = [physicsClient.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                                            halfExtents=raw_elements[0]["halfExtents"])]
            linkVisualShapeIndices = [-1]

            if view:
                texture_path = None
                for t in self.__texture_paths:
                    if raw_elements[0]["product_code"].lower() in t.lower():
                        texture_path = t
                        break
                try:
                    px, py, pz = self.__order.get_position_from_name(raw_elements[0]["product_code"].lower())
                    x, y, z = [r * 2 for r in raw_elements[0]["halfExtents"]]
                    px = - (x - px) / 2
                    py = - (y - py) / 2
                    pz = - (z - pz) / 2
                    shift = [px, py, pz]
                except KeyError:
                    texture_path = None
                if texture_path is not None:
                    linkCollisionShapeIndices = [
                        physicsClient.createCollisionShape(shapeType=pybullet.GEOM_BOX,
                                                           halfExtents=raw_elements[0]["halfExtents"])]
                    linkVisualShapeIndices = [physicsClient.createVisualShape(shapeType=pybullet.GEOM_MESH,
                                                                              fileName=texture_path,
                                                                              rgbaColor=[0.5, 0.3, 0.1, 1],
                                                                              visualFramePosition=shift)]
                else:
                    print("Warning: Texture not found for product code: " + raw_elements[0][
                        "product_code"] + " in specified texture dirs and subdirs")

            linkPositions = [raw_elements[0]["halfExtents"]]
            linkOrientations = [[0, 0, 0, 1]]
            linkInertialFramePositions = [[0, 0, 0]]
            linkInertialFrameOrientations = [[0, 0, 0, 1]]
            indices = [0]
            jointTypes = [pybullet.JOINT_PRISMATIC]
            axis = [[1, 0, 0]]
            index_base_pos = 0
            if test_data["axis"] == "y":
                axis = [[0, 1, 0]]
                index_base_pos = 1
            elif test_data["axis"] == "z":
                axis = [[0, 0, 1]]
                index_base_pos = 2

            pallet_id = physicsClient.createMultiBody(baseMass=0,
                                                      linkMasses=link_Masses,
                                                      linkCollisionShapeIndices=linkCollisionShapeIndices,
                                                      linkVisualShapeIndices=linkVisualShapeIndices,
                                                      linkPositions=linkPositions,
                                                      linkOrientations=linkOrientations,
                                                      linkInertialFramePositions=linkInertialFramePositions,
                                                      linkInertialFrameOrientations=linkInertialFrameOrientations,
                                                      linkParentIndices=indices,
                                                      linkJointTypes=jointTypes,
                                                      linkJointAxis=axis)

            # add mesh file to pallet
            physicsClient.changeVisualShape(pallet_id, -1, rgbaColor=[1, 1, 1, 1])

            elements = []
            for element in raw_elements[1:]:
                elements.append(self.__create_pybullet_element(physicsClient, element))

            targetPosition = 5
            currentTargetPosition = 0
            maxVelocity = .75
            force = 1300

            period_time = 0
            sim_time = 0
            change_ban = False
            factor = test_data["factor"]

            while sim_time < test_data["duration"]:
                physicsClient.stepSimulation()

                if view or not (thread_pallets or thread_tests):
                    if self.__loop_callback is not None:
                        self.__loop_callback({
                            "pallet": f"{i + 1}/{len(self.__order)}" if pallet_nr == "all" else "1/1",
                            "test number": test_index_data + 1,
                            "time": f"{round(sim_time, 4)}/{test_data['duration']}s",
                        })

                if not change_ban:
                    if sim_time >= test_data["change_time"]:
                        factor = - factor
                        change_ban = True

                if period_time + test_data["period"] < sim_time and factor != 0:
                    currentTargetPosition += factor
                    period_time = sim_time
                    if abs(currentTargetPosition) > targetPosition:
                        currentTargetPosition = targetPosition if currentTargetPosition > 0 else -targetPosition
                    physicsClient.setJointMotorControl2(pallet_id, 0, pybullet.POSITION_CONTROL,
                                                        maxVelocity=maxVelocity,
                                                        targetPosition=targetPosition if currentTargetPosition > 0 else
                                                        -targetPosition, force=force)

                    if view:
                        basePos = list(physicsClient.getBasePositionAndOrientation(pallet_id)[0])
                        basePos[index_base_pos] += physicsClient.getJointState(pallet_id, 0)[0]

                        cameraYaw = physicsClient.getDebugVisualizerCamera()[8]
                        cameraPitch = physicsClient.getDebugVisualizerCamera()[9]

                        physicsClient.resetDebugVisualizerCamera(cameraDistance=4, cameraYaw=cameraYaw,
                                                                 cameraPitch=cameraPitch,
                                                                 cameraTargetPosition=basePos)  # fix camera onto model

                    for sim_box in elements:
                        if physicsClient.getContactPoints(sim_box, plane_id):
                            physicsClient.disconnect()
                            results["pallets"][pallet_nr_index]["testResults"][test_index_data] = False
                            return
                sim_time += 1 / 240.
            physicsClient.disconnect()
            results["pallets"][pallet_nr_index]["testResults"][test_index_data] = True

        results = {
            "testsNames": [test["name"] for test in self.tests],
            "pallets": []
        }

        local_test_data = []
        for test in self.tests:
            axs = test["name"].split(" ")[0].lower()
            if axs not in ["x", "y", "z"]:
                axs = "y"
                fctr = 0
            else:
                fctr = max([step[f"force_{axs}"] for step in test["steps"]])
                # test["duration"] *= 2
            local_test_data.append({
                'duration': test["duration"],
                'period': max([step["period"] for step in test["steps"]]),
                'axis': axs,
                'factor': fctr,
                'change_time': test["duration"] / 2,
                "name": test["name"]
            })

        def do_pallet(raw_pallet_data_t, pos_index):
            tests_threads = []
            for j, test in enumerate(local_test_data):
                if thread_tests and not view:
                    tests_threads.append(
                        threading.Thread(target=run_test, args=(raw_pallet_data_t, test, pos_index, j), daemon=True))
                    tests_threads[-1].start()
                else:
                    run_test(raw_pallet_data_t, test, pos_index, j)
            for tests_thread in tests_threads:
                tests_thread.join()

        pallet_threads = []
        for i, raw_pallet_data in enumerate(self.__order.iterate_models_data("pybullet")):
            if pallet_nr not in [self.__order.get_pallet_nr(i), "all"]:
                continue

            results["pallets"].append({
                "palletNr": self.__order.get_pallet_nr(i),
                "index": i,
                "testResults": [None] * len(self.tests)
            })

            if thread_pallets and not view:
                pallet_threads.append(
                    threading.Thread(target=do_pallet, args=(raw_pallet_data, len(results["pallets"]) - 1,),
                                     daemon=True))
                pallet_threads[-1].start()
            else:
                do_pallet(raw_pallet_data, len(results["pallets"]) - 1)

        total_pallet_threads = len(pallet_threads)
        while len(pallet_threads) > 0:
            pallet_threads = [thread for thread in pallet_threads if thread.is_alive()]
            if self.__loop_callback is not None:
                self.__loop_callback({
                    "pallets done": f"{total_pallet_threads - len(pallet_threads)}/{total_pallet_threads}"
                })
            time.sleep(0.1)

        return results

    def __run_mujoco_simulation(self, view: bool = False, pallet_nr: str = "all", color_by: str = "product_code",
                                fps: int = 60, thread_tests: bool = True, thread_pallets: bool = True) -> dict:
        def simulate_pallet(model_str: str, index: int) -> None:

            def run_test(model: mujoco.MjModel, data: mujoco.MjData, test: dict, num_test: int) -> None:
                if len(test["steps"]) == 0:
                    return
                current_time = 0
                sub_step_index = 0
                counter = fps - 1
                if view:
                    viewer.change_model(model)
                    width, height = viewer.get_dimensions()
                while current_time < test["duration"]:
                    mujoco.mj_step1(model, data)

                    if view or not (thread_pallets or thread_tests):
                        counter += 1
                        if self.__loop_callback is not None:
                            self.__loop_callback({
                                "pallet": f"{i + 1}/{len(self.__order)}" if pallet_nr == "all" else "1/1",
                                "test": test["name"],
                                "time": f"{round(data.time, 4)}/{test['duration']}s",
                            })

                    if view and counter == fps:
                        counter = 0
                        imgs = {
                            "width": width,
                            "height": height,
                            "imgs": {
                                "fixed": viewer.read_pixels(data, 0),
                                "corner": viewer.read_pixels(data, 1),
                                "top": viewer.read_pixels(data, 2)
                            }
                        }

                        if self.__img_callback is not None:
                            self.__img_callback(imgs)

                    if sub_step_index + 1 < len(test["steps"]):
                        if test["steps"][sub_step_index + 1]["time"] <= data.time:
                            sub_step_index += 1
                    step = test["steps"][sub_step_index]

                    if current_time + step["period"] < data.time:
                        data.ctrl[0] += step["force_x"]
                        data.ctrl[1] += step["force_y"]
                        current_time = data.time

                    mujoco.mj_step2(model, data)
                    for body in range(model.nbody):
                        if data.xpos[body][2] < 0:
                            return

                res["testResults"][num_test] = True

            res = {
                "palletNr": self.__order.get_pallet_nr(index),
                "index": index,
                "testResults": [False for _ in range(len(self.tests))]
            }

            model_g = mujoco.MjModel.from_xml_string(model_str, self.__assets)
            data_g = mujoco.MjData(model_g)
            if view or not thread_tests:
                for test_index, pallet_test in enumerate(self.tests):
                    run_test(copy.deepcopy(model_g), copy.deepcopy(data_g), pallet_test, test_index)
            else:
                tests_threads = list()
                for test_index, pallet_test in enumerate(self.tests):
                    tests_threads.append(threading.Thread(target=run_test, args=(
                        copy.deepcopy(model_g), copy.deepcopy(data_g), pallet_test, test_index)))
                    tests_threads[-1].start()
                total_test_threads = len(tests_threads)
                while len(tests_threads) > 0:
                    tests_threads = [thread for thread in tests_threads if thread.is_alive()]
                    if not thread_pallets and self.__loop_callback is not None:
                        self.__loop_callback({
                            "pallet": f"{i + 1}/{len(self.__order)}" if pallet_nr == "all" else "1/1",
                            "Tests done": f"{total_test_threads - len(tests_threads)}/{total_test_threads}"
                        })
                    time.sleep(0.1)
            results["pallets"].append(res)

        if view:
            viewer = MujocoViewer()

        results = {
            "testsNames": [test["name"] for test in self.tests],
            "pallets": list()
        }

        pallet_threads = []
        for i, raw_pallet_data in enumerate(
                self.__order.iterate_models_data("mujoco", color_by=color_by, use_generic_pallet=False)):
            if pallet_nr not in [self.__order.get_pallet_nr(i), "all"]:
                continue

            if not view and thread_pallets:
                pallet_threads.append(threading.Thread(target=simulate_pallet, args=(raw_pallet_data, i), daemon=True))
                pallet_threads[-1].start()
            else:
                simulate_pallet(raw_pallet_data, i)

        total_pallet_threads = len(pallet_threads)
        while len(pallet_threads) > 0:
            pallet_threads = [thread for thread in pallet_threads if thread.is_alive()]
            if self.__loop_callback is not None:
                self.__loop_callback({
                    "pallets done": f"{total_pallet_threads - len(pallet_threads)}/{total_pallet_threads}"
                })
            time.sleep(0.1)

        if view:
            viewer.close()

        # sort the "pallets" by the index
        results["pallets"] = sorted(results["pallets"], key=lambda pallet: pallet["index"])
        return results


def pretty_print(results, header=""):
    if header:
        print(header + ":")
    else:
        print("Results:")
    for pallet in results["pallets"]:
        print(f"\tPallet {pallet['palletNr']}")
        for i in range(len(pallet["testResults"])):
            print(f"\t\t{results['testsNames'][i]}: {pallet['testResults'][i]}")
    print()


# main function to test the class and the simulation
def demo():
    def callback(imgs):
        imgs = imgs["imgs"]
        cv2.imshow("fixed", imgs["fixed"])
        cv2.imshow("top", imgs["top"])
        cv2.imshow("corner", imgs["corner"])
        cv2.waitKey(1)

    code = "0615615"
    pallet_sim = Pallet_Sim(img_callback=callback)

    path = pkg_resources.resource_filename(__name__, rf"example_data/{code}")
    order = open(path + ".order.json").read()
    if not pallet_sim.load(json_data=order):
        print("Failed to load order from json")
        return

    result_json = pallet_sim.run_simulation(view=True)
    pretty_print(result_json, "JSON")

    # # check if the results are the same
    # equal = True
    # for i in range(len(result_xml["pallets"])):
    #     for j in range(len(result_xml["pallets"][i]["testResults"])):
    #         if result_xml["pallets"][i]["testResults"][j] != result_json["pallets"][i]["testResults"][j]:
    #             print(f"Results are different for pallet {i} and test {j} :(")
    #             equal = False
    # if equal:
    #     print("Results are the same :)")

    pallet_sim.run_simulation(pallet_nr=pallet_sim.get_pallet_nr(0), view=True, color_by="weight", fps=120)


def pybullet_and_mujoco_test():
    code = "0615615"
    pallet_sim = Pallet_Sim()

    if not pallet_sim.load(json_data=pkg_resources.resource_filename(__name__, rf"./example_data/{code}.order.json")):
        print("Failed to load order from file")
        return

    # pallet_sim.load_order_from_path("U1418507.0615622.pal.xml")
    t = time.time()
    result_pybullet = pallet_sim.run_simulation(simulation_engine="pybullet")
    print(f"Pybullet simulation took {time.time() - t} seconds")
    pretty_print(result_pybullet, "PyBullet")

    t = time.time()
    result_mujoco = pallet_sim.run_simulation(simulation_engine="mujoco")
    print(f"Mujoco simulation took {time.time() - t} seconds")
    pretty_print(result_mujoco, "Mujoco")

    # check if the results are the same
    equal = True
    for i in range(len(result_pybullet["pallets"])):
        for j in range(len(result_pybullet["pallets"][i]["testResults"])):
            if result_pybullet["pallets"][i]["testResults"][j] != result_mujoco["pallets"][i]["testResults"][j]:
                print(f"Results are different for pallet {i} and test {j} :(")
                equal = False
    if equal:
        print("Results are the same :)")


def threading_speed_test(simulation_method="pybullet", view=False, fps=120):
    def time_function(function, *args, **kwargs):
        t = time.time()
        function(*args, **kwargs)
        return time.time() - t

    code = "0615615"
    pallet_sim = Pallet_Sim()

    if not pallet_sim.load(json_data=pkg_resources.resource_filename(__name__, rf"./example_data/{code}.order.json")):
        print("Failed to load order from file")
        return

    kwargs = {
        "simulation_engine": simulation_method,
        "view": view,
        "fps": fps,
        "thread_pallets": False,
        "thread_tests": False
    }

    sim_no_threads_time = time_function(pallet_sim.run_simulation, **kwargs)

    kwargs["thread_tests"] = True
    sim_tests_threads_time = time_function(pallet_sim.run_simulation, **kwargs)

    kwargs["thread_tests"] = False
    kwargs["thread_pallets"] = True
    sim_pallets_threads_time = time_function(pallet_sim.run_simulation, **kwargs)

    kwargs["thread_tests"] = True
    sim_both_threads_time = time_function(pallet_sim.run_simulation, **kwargs)

    # make table of results
    print()
    print(f"{'Simulation method':<20}{'No threads':<20}{'Tests threaded':<20}"
          f"{'Pallets threaded':<20}{'Both threaded':<20}")
    print(f"{simulation_method.capitalize():<20}{sim_no_threads_time:<20.2f}{sim_tests_threads_time:<20.2f}"
          f"{sim_pallets_threads_time:<20.2f}{sim_both_threads_time:<20.2f}")
    # print speedup percentage with a percentage sign
    print(f"{'Speedup percentage':<20}{'-':<20}"
          f"{(sim_no_threads_time / sim_tests_threads_time - 1) * 100:<20.2f}"
          f"{(sim_no_threads_time / sim_pallets_threads_time - 1) * 100:<20.2f}"
          f"{(sim_no_threads_time / sim_both_threads_time - 1) * 100:<20.2f}")
    print()


def test_view():
    code = "0615615"
    pallet_sim = Pallet_Sim()

    if not pallet_sim.load(json_data=pkg_resources.resource_filename(__name__, rf"./example_data/{code}.order.json")):
        print("Failed to load order from file")
        return
    pallet_sim.show_3D_pallet(1)


if __name__ == '__main__':
    test_view()
    demo()
    # pybullet_and_mujoco_test()
    # pybullet_and_mujoco_test()

    pybullet_and_mujoco_test()

    threading_speed_test()
    print("-" * 100)
    threading_speed_test("mujoco")
