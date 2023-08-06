import copy
import json
import os
import random
import pkg_resources
from xml.dom.minidom import parseString

from .xml_obfuscator import obfuscate_xml

import numpy as np
import stl


# class for handling an order, loading the data and generating the models in different formats (mujoco,
# pybullet) initialization requires a path to a .pal.xml file (and there to exists an ord.xml file on the same path)
# or a json string that contains the following keys: pallet, article an and optinal orderID. the class
# can be used to generate a mujoco model, a pybullet model and a json string with the model data and article data it
# is primarily used by the pallet simulator to get the input data for the simulation
class Order:
    def __init__(self, *, json_data: str | dict = None, path_data: str = None, load_method: str | None = None,
                 texture_paths: list | str = None) -> None:
        self.__pallets = []
        self.__articles = {}
        self.__order_id = None

        # if json_data and path_data are both None, raise an error
        if json_data is None and path_data is None:
            raise ValueError('No data given')

        # if json_data and path_data are given but no load_method, raise an error
        if json_data is not None and path_data is not None and load_method is None:
            raise ValueError('No load method given can not infer load method from arguments')

        if load_method is None:
            # infer the load method from the arguments
            if json_data is not None:
                load_method = "json"
            else:
                load_method = "xml"
        load_method = load_method.lower()

        if load_method == "xml":
            # check path_data is not None and call the __load_from_xml method
            if path_data is None:
                raise ValueError('No path given for xml load method')
            self.__load_from_xml(path_data)
        elif load_method == "json":
            # check json_data is not None and call the __load_from_json method
            if json_data is None:
                raise ValueError('No json data given for json load method')
            self.__load_from_json(json_data)
        else:
            raise ValueError("load_method must be 'xml' or 'json'")
        self.__palletNrs = [pallet["palletNr"] for pallet in self.__pallets]

        if texture_paths is str:
            texture_paths = [texture_paths]
        if texture_paths is None:
            if os.path.isdir(pkg_resources.resource_filename(__name__, "./textures")):
                texture_paths = [pkg_resources.resource_filename(__name__, "./textures")]
            else:
                texture_paths = []

        self.__pallets_position_from_stl = {}
        for texture in texture_paths:
            if os.path.isfile(texture) and (texture.endswith(".stl")):
                # save without the extension
                self.__pallets_position_from_stl[
                    os.path.basename(texture)[:-4].lower()] = self.get_positions_from_mesh_file(
                    texture)
                # self.__stl_files[os.path.basename(texture)] = self.get_positions(texture)
            elif os.path.isdir(texture):
                for file in os.listdir(texture):
                    if file.endswith(".stl"):
                        # save without the extension
                        self.__pallets_position_from_stl[
                            os.path.basename(file)[:-4].lower()] = self.get_positions_from_mesh_file(
                            os.path.join(texture, file))
                        # self.__stl_files[file] = self.get_positions(os.path.join(texture, file))
            else:
                raise Exception("Texture not found")

    def __len__(self):
        return len(self.__pallets)

    def __str__(self):
        return "Order: " + self.__order_id + "\n\nPallets:\n" + json.dumps(self.__pallets,
                                                                           indent=4) + "\n\nArticles:\n" + json.dumps(
            self.__articles, indent=4)

    def get_position_from_name(self, name: str) -> tuple[float, float, float]:
        return self.__pallets_position_from_stl[name.lower()]

    def get_pallet_nrs(self) -> list:
        return self.__palletNrs

    def get_pallet_nr(self, pallet_index: int) -> str:
        if pallet_index >= len(self.__pallets):
            raise ValueError(f'Invalid pallet index: {pallet_index}')
        return copy.deepcopy(self.__pallets[pallet_index]["palletNr"])

    def get_model_data(self, model_type: str, pallet_index: int, **kwargs) -> list[dict] | str:
        model_type = model_type.lower()
        if model_type not in self.model_types:
            raise ValueError(f'Invalid model type: {model_type}')
        if pallet_index >= len(self.__pallets):
            raise ValueError(f'Invalid pallet index: {pallet_index}')
        if model_type == "mujoco":
            if "color_by" in kwargs and kwargs["color_by"] not in self.color_by_options:
                raise ValueError(f'Invalid color_by option: {"color_by"}')
            return self.__export_pallet_to_mujoco(pallet_index, **kwargs)
        return self.__export_pallet_to_pybullet(pallet_index)

    def iterate_models_data(self, model_type: str, **kwargs) -> iter:
        model_type = model_type.lower()
        if model_type not in self.model_types:
            raise ValueError(f'Invalid model type: {model_type}')
        if model_type == "mujoco":
            if "color_by" in kwargs and kwargs["color_by"] not in self.color_by_options:
                raise ValueError(f'Invalid color_by option: {"color_by"}')
            for pallet_index in range(len(self.__pallets)):
                yield self.__export_pallet_to_mujoco(pallet_index, **kwargs)
        else:
            for pallet_index in range(len(self.__pallets)):
                yield self.__export_pallet_to_pybullet(pallet_index)

    def get_id(self) -> str:
        return self.__order_id

    def get_pallet(self, pallet_index: int) -> dict:
        if pallet_index >= len(self.__pallets):
            raise ValueError(f'Invalid pallet index: {pallet_index}')
        return copy.deepcopy(self.__pallets[pallet_index])

    def __load_from_xml(self, pal_path: str) -> None:
        self.__load_from_json(obfuscate_xml(pal_path))

    def __load_from_json(self, order_data: dict | str) -> None:
        # check if the order_data is a dict or a string and load it
        if type(order_data) == str:
            order_data = json.loads(order_data)
        # check if it has all the required keys (pallets, articles) and if orderID is not present, set it to None
        if "pallets" not in order_data or "articles" not in order_data:
            raise ValueError("Invalid order data")
        self.__order_id = order_data["orderID"] if "orderID" in order_data else ""

        # load the pallets and articles
        pal = order_data["pallets"]
        art = order_data["articles"]

        self.__pallets = []
        for pallet in pal:
            for box in pallet["boxes"]:
                try:
                    box["rgb"] = art[box["product_code"]]["rgb"]
                except KeyError:
                    art[box["product_code"]]["rgb"] = [round(random.uniform(0.1, 0.9), 3) for _ in range(3)]
                    box["rgb"] = art[box["product_code"]]["rgb"]
                box["weight"] = art[box["product_code"]]["weight"]
            self.__pallets.append(self.__change_pallet_type_helper(pallet))
        self.__articles = art

    @staticmethod
    def __change_pallet_type_helper(pallet: dict) -> dict:
        pal = pallet["palletType"].lower()
        if pal.count("euro") > 0:
            pallet["palletType"] = "Euro_Pallet"
            if pallet["palletDimension"]["x"] > pallet["palletDimension"]["y"]:
                pallet["palletType"] += "_Rotated"
        elif pal.count("ü") > 0 or pal.replace("ü", "u").count("duesseldorfer") > 0:
            pallet["palletType"] = "Duesseldorfer_Pallet"
            if pallet["palletDimension"]["x"] < pallet["palletDimension"]["y"]:
                pallet["palletType"] += "_Rotated"
                print("Rotated")

        if pallet["palletType"].count("US") > 0:
            print("US pallets are not supported yet")
        return pallet

    # color_by = "product_code" | "shipping_group" | "weight"
    def __export_pallet_to_mujoco(self, pallet_index: int, color_by: str = "product_code",
                                  use_generic_pallet: bool = False) -> str:
        if self.__pallets is None:
            raise ValueError('No order loaded')
        if pallet_index >= len(self.__pallets):
            raise ValueError(f'Invalid pallet index: {pallet_index}')

        document = parseString(self.base_xml)

        colorList = dict()
        if color_by == "product_code":
            for articleID, article in self.__articles.items():
                colorList[articleID] = [round(random.uniform(0.1, 0.9), 3) for _ in range(3)]
                colorList[articleID].append(1)
        elif color_by == "weight":
            # get the max weight and min weight and create a color gradient for elements and add it to the color list
            # with range 0.2 - 0.8 where 0.2 means it's lightest and 0.8 means it's the heaviest
            max_weight = 0
            min_weight = 100_000_000
            for article in self.__articles.values():
                max_weight = max(max_weight, article["weight"])
                min_weight = min(min_weight, article["weight"])

            if max_weight == min_weight and len(self.__articles) == 1:
                # make all boxes the same color
                for articleID in self.__articles.keys():
                    colorList[articleID] = [0.5, 0.5, 0.5, 1]
            else:
                for articleID, article in self.__articles.items():
                    colorList[articleID] = [
                        round((article["weight"] - min_weight) / (max_weight - min_weight) * 0.6 + 0.2, 3) for _ in
                        range(3)]
                    colorList[articleID].append(1)
        elif color_by == "shipping_group":
            # each self.articles has a non-unique shipping group, create a color for each shipping group and add it
            # to the color list by article id
            groupsColor = {}
            for article in self.__articles.values():
                groupsColor[article["shippingGroup"]] = [round(random.uniform(0.1, 0.9), 3) for _ in range(3)]
                groupsColor[article["shippingGroup"]].append(1)
            try:
                for articleID, article in self.__articles.items():
                    colorList[articleID] = groupsColor[article["shippingGroup"]]
            except KeyError:
                print(f"Article {articleID} has no shipping group")
        else:
            raise ValueError(f"Invalid color_by: {color_by}")

        pallet: dict = self.__pallets[pallet_index]
        ptype = pallet['palletType'].lower()
        document.getElementsByTagName("asset")[0].getElementsByTagName("mesh")[0].setAttribute("file",
                                                                                               f"{ptype}.stl")
        # print("Pallet type: " + ptype)

        for body in document.getElementsByTagName("body"):
            if body.getAttribute("name") == "pallet":
                p = body.getElementsByTagName("geom")[0]
                dim_x = round(pallet["palletDimension"]["x"] / 1000, 5)
                dim_y = round(pallet["palletDimension"]["y"] / 1000, 5)
                dim_z = .144
                p.setAttribute("size", f"{dim_x} {dim_y} {dim_z}")
                p.setAttribute("pos", f"{dim_x} {dim_y} -{dim_z}")
                p.setAttribute("mass", "25")
                p.setAttribute("group", "3")
                p.setAttribute("rgba", "0.5 0.3 0.1 1")

                # body.getElementsByTagName("geom")[1].setAttribute("pos", f"{w - 0.24} {l} -.02")
                vp = body.getElementsByTagName("geom")[1]
                vp.setAttribute("rgba", "0.5 0.3 0.1 1")  # brown
                vp.setAttribute("size", f"{dim_x} {dim_y} {dim_z}")
                if not use_generic_pallet:
                    if ptype in self.__pallets_position_from_stl:
                        pallet_w, pallet_l, _ = self.__pallets_position_from_stl[ptype]
                        vp.setAttribute("pos", f"{pallet_w} {pallet_l} -.02")
                    else:
                        print(
                            f"Warning: pallet type {ptype} not found in pallets position from stl, using generic pallet")
                        # if len(self.__pallets_position_from_stl) > 0:
                        #     pallet_w, pallet_l, _ = list(self.__pallets_position_from_stl.values())[0]
                        #     document.getElementsByTagName("asset")[0].getElementsByTagName("mesh")[0].setAttribute(
                        #         "file", f"{list(self.__pallets_position_from_stl.keys())[0]}.stl")
                        #     vp.setAttribute("pos", f"{pallet_w} {pallet_l} -.02")
                        # else:
                        #     print("Warning: no pallets position from stl found, deleting pallet")
                        use_generic_pallet = True

                if use_generic_pallet:
                    document.getElementsByTagName("asset")[0].removeChild(
                        document.getElementsByTagName("asset")[0].getElementsByTagName(
                            "mesh")[0])
                    # delete vp for body pallet
                    body.removeChild(vp)
                    # vp.setAttribute("group", "3")
                    p.setAttribute("group", "1")

                for camera in document.getElementsByTagName("camera"):
                    name = camera.getAttribute("name")
                    if name == "top":
                        camera.setAttribute("pos", f"{round(dim_x / 2, 5)} {round(dim_y / 2, 5)} 9")
                    elif name == "corner":
                        camera.setAttribute("pos", f"-{dim_x * 2.5} -6 2")

        world_body = document.getElementsByTagName("worldbody")[0]
        joint = document.createElement("joint")
        joint.setAttribute("type", "free")
        for index in range(len(pallet["boxes"])):
            # for index in range(r):
            box = pallet["boxes"][index]
            body = document.createElement("body")
            # body.setAttribute("articleID", box.product_code)
            body.setAttribute("name", str(index))

            box_x, box_y, box_z = box['anchor']['x'], box['anchor']['y'], box['anchor']['z']
            box_x = round(box_x / 1000, 5)
            box_y = round(box_y / 1000, 5)
            box_z = round(box_z / 1000, 5)
            dim_x, dim_y, dim_z = box['dimension']['x'], box['dimension']['y'], box['dimension']['z']
            dim_x = round(dim_x / 1000, 5)
            dim_y = round(dim_y / 1000, 5)
            dim_z = round(dim_z / 1000, 5)

            box_x = 2 * box_x + dim_x
            box_y = 2 * box_y + dim_y
            box_z = 2 * box_z + dim_z

            body.setAttribute("pos", f"{box_x} {box_y} {box_z}")
            geom = document.createElement("geom")
            # type="box", size, rgba, mass
            geom.setAttribute("type", "box")
            geom.setAttribute("size", f"{dim_x} {dim_y} {dim_z}")

            try:
                geom.setAttribute("rgba", " ".join(map(str, colorList[box["product_code"]])))
            except KeyError:
                if color_by == "product_code":
                    colorList[box["product_code"]] = [round(random.uniform(0.1, 0.9), 3) for _ in range(3)]
                    colorList[box["product_code"]].append(1)
                    geom.setAttribute("rgba", " ".join(map(str, colorList[box["product_code"]])))
                else:
                    # if the color_by is not product_code, then the colorList should contain the information for the
                    # colorization that is needed, so if the key is not found, then it is an error and should be
                    # reported
                    raise KeyError("Key not found in colorList: {}".format(box["product_code"]))

            # geom.setAttribute("rgba", f"{box['rgb'][0]} {box['rgb'][1]} {box['rgb'][2]} 1")

            # mass is stored in the article data
            geom.setAttribute("mass", f"{self.__articles[box['product_code']]['weight']}")
            body.appendChild(geom)
            body.appendChild(joint.cloneNode(True))
            world_body.appendChild(body)
        return document.getElementsByTagName("mujoco")[0].toxml()

    def __export_pallet_to_pybullet(self, pallet_index: int) -> list[dict]:
        if self.__pallets is None:
            raise ValueError('No order loaded')
        if pallet_index >= len(self.__pallets):
            raise ValueError(f'Invalid pallet index: {pallet_index}')

        pallet = self.__pallets[pallet_index]
        dim_x = round(pallet["palletDimension"]["x"] / 1000, 5)
        dim_y = round(pallet["palletDimension"]["y"] / 1000, 5)
        dim_z = .144
        elements_data = [{
            "product_code": pallet["palletType"],
            "basePosition": [dim_x / 2, dim_y / 2, dim_z / 2],
            "halfExtents": [dim_x / 2, dim_y / 2, dim_z / 2],
            "baseMass": 25
        }]
        # create the boxes
        for box in pallet["boxes"]:
            box_x, box_y, box_z = box['anchor']['x'], box['anchor']['y'], box['anchor']['z']
            dim_x, dim_y, dim_z = box['dimension']['x'], box['dimension']['y'], box['dimension']['z']

            box_x = round((2 * box_x + dim_x) / 2000, 5)
            box_y = round((2 * box_y + dim_y) / 2000, 5)
            box_z = round((2 * box_z + dim_z) / 2000, 5) + .144

            dim_x = round(dim_x / 2000, 5)
            dim_y = round(dim_y / 2000, 5)
            dim_z = round(dim_z / 2000, 5)

            elements_data.append({
                "product_code": box["product_code"],
                "basePosition": [box_x, box_y, box_z],
                "halfExtents": [dim_x, dim_y, dim_z],
                "baseMass": self.__articles[box["product_code"]]["weight"],
            })
        return elements_data

    @staticmethod
    def get_positions_from_mesh_file(mesh_file: str) -> tuple[float, float, float]:
        # read the mesh file
        # m = mesh.Mesh.from_file('textures/Euro_Pallet.stl')
        m = stl.mesh.Mesh.from_file(mesh_file)
        # get the corner points of the mesh
        corner_points = m.vectors
        # get the x,y,z coordinates of the corner points
        x = corner_points[:, :, 0]
        y = corner_points[:, :, 1]
        z = corner_points[:, :, 2]

        # get the min and max values of the corner points
        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)
        zmin = np.min(z)
        zmax = np.max(z)

        # get the center of the mesh
        xc = (xmin + xmax) / 2
        yc = (ymin + ymax) / 2
        zc = (zmin + zmax) / 2

        # get the size of the mesh
        xsize = xmax - xmin
        ysize = ymax - ymin
        zsize = zmax - zmin

        return round((xsize / 2 - xc) * 2, 2), round((ysize / 2 - yc) * 2, 2), round((zsize / 2 - zc) * 2, 2)

    model_types = ["mujoco", "pybullet"]
    color_by_options = ["product_code", "weight", "shipping_group"]

    base_xml = """
        <mujoco>
            <option timestep=".004">
            </option>

            <size memory="-1"/>
            
            <asset>
                <material name="pallet" specular="1" shininess="1"/>
                <mesh name="pallet" file="" scale="2 2 2"/>
            </asset>

            <visual>
                <quality shadowsize="0"/>
                <headlight ambient=".5 .5 .5" diffuse=".5 .5 .5" specular=".5 .5 .5"/>
            </visual>
            
            <default>
                <geom type="box" friction=".5"/>
            </default>
             
            <worldbody>
                <body name="floor">
                    <geom type="plane" size="20 20 .01" pos="0 0 -5"/>
                </body>

                <camera name="fixed" pos="-10 -25 2" euler="90 -45 0" mode="targetbody" target="pallet"/>         

                <body name="pallet">
                    <geom type="box" friction=".5" rgba=".9 0 0 1"/>
                    <geom type="mesh" mesh="pallet" euler="0 0 0" group="1"/>
                    <joint name="conveyor x" type="slide" damping="5000" axis="1 0 0"/>
                    <joint name="conveyor y" type="slide" damping="5000" axis="0 1 0"/>
                    <camera name="corner" pos="-2 -6 2" euler="90 -20 0" mode="track"/>
                    <camera name="top" pos=".8 .6 9" mode="track"/>
                </body>

            </worldbody>

            <actuator>
                <position name="conveyor x" joint="conveyor x" ctrlrange="-10 10" ctrllimited="true" kp="4000"/>
                <position name="conveyor y" joint="conveyor y" ctrlrange="-10 10" ctrllimited="true" kp="4000"/>
            </actuator>
        </mujoco>
    """


# main function for testing.py purposes only
def demo() -> None:
    import mujoco
    import time
    import os
    import tqdm

    path = pkg_resources.resource_filename(__name__, r"./example_data/0615610.order.json")
    order = Order(json_data=open(path, "r").read())
    model = mujoco.MjModel.from_xml_string(order.get_model_data(model_type="mujoco", pallet_index=0), {
        os.path.basename(asset).lower(): open(pkg_resources.resource_filename(__name__, f"./textures/{asset}"),
                                              "rb").read() for asset in
        os.listdir(pkg_resources.resource_filename(__name__, "./textures"))
    })
    data = mujoco.MjData(model)

    times = 10_000
    t = time.time()
    for _ in tqdm.tqdm(range(times), desc="Running simulation", unit="step"):
        mujoco.mj_step1(model, data)
        mujoco.mj_step2(model, data)

    t1 = time.time() - t

    mujoco.mj_resetData(model, data)
    t = time.time()
    for _ in tqdm.tqdm(range(times), desc="Running simulation", unit="step"):
        mujoco.mj_step(model, data)

    t2 = time.time() - t
    print(f"Time for {times} steps: {t1} seconds")
    print(f"Time for {times} steps: {t2} seconds")


if __name__ == "__main__":
    demo()
