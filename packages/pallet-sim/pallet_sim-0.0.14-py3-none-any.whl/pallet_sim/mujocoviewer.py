import glfw
import numpy as np
import mujoco


# class to interact with mujoco to get images from specific cameras used to display while the simulation is running
# after initialization, call read_pixels() to get the raw image data from the camera
# change_model() can be used to change the model being used to get the image data
class MujocoViewer:
    def __init__(self, *, width: int = 500, height: int = 500, model: mujoco.MjModel = None, hide: bool = True) -> None:
        self.__ctx = None
        self.__scn = None
        self.__width = width
        self.__height = height
        self.__model = model
        self.__hide = hide

        glfw.init()

        if hide:
            glfw.window_hint(glfw.VISIBLE, 0)
        else:
            # add event handlers for ctr + move to move the camera around
            pass
        self.__window = glfw.create_window(width, height, "Test", None, None)
        glfw.make_context_current(self.__window)
        glfw.swap_interval(1)
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self.__window)

        self.__vopt = mujoco.MjvOption()
        self.__cam = mujoco.MjvCamera()
        self.__pert = mujoco.MjvPerturb()

        # get viewport
        self.__viewport = mujoco.MjrRect(0, 0, framebuffer_width, framebuffer_height)
        if model is not None:
            self.change_model(model)

    def get_dimensions(self) -> (int, int):
        return self.__width, self.__height

    def change_model(self, model: mujoco.MjModel) -> None:
        model_was_not_set = self.__model is None
        self.__model = model
        self.__scn = mujoco.MjvScene(model, maxgeom=10000)
        self.__ctx = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150.value)
        if model_was_not_set:
            mujoco.mjv_moveCamera(model, mujoco.mjtMouse.mjMOUSE_ZOOM, 0, -2, self.__scn, self.__cam)

    # get the pixels from the current scene
    def read_pixels(self, data: mujoco.MjData, cam_id: int = None):
        if cam_id is not None:
            if cam_id == -1:
                self.__cam.type = mujoco.mjtCamera.mjCAMERA_FREE
            else:
                self.__cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
            self.__cam.fixedcamid = cam_id

        if self.__scn is None or self.__ctx is None:
            raise Exception("No scene or context set")

        self.__viewport.width, self.__viewport.height = glfw.get_framebuffer_size(self.__window)
        # update scene
        mujoco.mjv_updateScene(self.__model, data, self.__vopt, self.__pert, self.__cam,
                               mujoco.mjtCatBit.mjCAT_ALL.value, self.__scn)
        # render
        mujoco.mjr_render(self.__viewport, self.__scn, self.__ctx)

        img = np.zeros((glfw.get_framebuffer_size(self.__window)[1], glfw.get_framebuffer_size(self.__window)[0], 3),
                       dtype=np.uint8)
        mujoco.mjr_readPixels(img, None, self.__viewport, self.__ctx)
        return np.flipud(img)

    def close(self) -> None:
        glfw.destroy_window(self.__window)
        glfw.terminate()
        if self.__ctx is not None:
            self.__ctx.free()
