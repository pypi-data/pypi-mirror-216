import json
import os
import threading
import time
import tkinter as tk
import ctypes
from tkinter import filedialog, messagebox
import pkg_resources

from .pallet_sim import Pallet_Sim
from .pallet_generator2D.g4algorithm import algorithm_artikel

from PIL import ImageTk, Image

class Pallet2D_Handler:
    class Box:
        def __init__(self, anchor: tuple[float], dimension: tuple[float]) -> None:
            # check the anchor length is between 2 and 3
            if len(anchor) not in (2, 3):
                raise ValueError("Anchor length must be 2 or 3")
            # check the dimension length is between 2 and 3
            if len(dimension) not in (2, 3):
                raise ValueError("Dimension length must be 2 or 3")
            if len(anchor) == 2:
                anchor = (anchor[0], anchor[1], 0)
            if len(dimension) == 2:
                dimension = (dimension[0], dimension[1], 100)
            self.__x, self.__y, self.__z = anchor
            self.__dimension_x, self.__dimension_y, self.__dimension_z = dimension

        def get_coordinates(self) -> tuple[int, int, int, int, int, int]:
            return self.__x, self.__y, self.__z, self.__x + self.__dimension_x, self.__y + self.__dimension_y, self.__z + self.__dimension_z

        def get_dim_x(self) -> int:
            return self.__dimension_x

        def get_dim_y(self) -> int:
            return self.__dimension_y

        def get_dim_z(self) -> int:
            return self.__dimension_z

        def export_to_json(self, *, product_code: str = "0", approach: str = "C") -> dict:
            return {
                "product_code": product_code,
                "anchor": {
                    "x": self.__x,
                    "y": self.__y,
                    "z": self.__z
                },
                "dimension": {
                    "x": self.__dimension_x,
                    "y": self.__dimension_y,
                    "z": self.__dimension_z
                },
                "approach": approach
            }

    def __init__(self, size: tuple[float, float], pallet_type: str = "Custom") -> None:
        self.__x, self.__y = size
        self.__pallet_type = pallet_type
        self.__boxes = []

    def __getitem__(self, item: int) -> Box:
        return self.__boxes[item]

    def __iter__(self) -> iter:
        return iter(self.__boxes)

    def __len__(self) -> int:
        return len(self.__boxes)

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def add(self, origin: tuple, size: tuple) -> None:
        self.__boxes.append(self.Box(origin, size))

    def get_name(self, *, two_2=True, index=None) -> str:
        pal_x, pal_y = self.get_x(), self.get_y()
        box_x, box_y = self[0].get_dim_x(), self[0].get_dim_y()
        if box_x < box_y:
            box_x, box_y = box_y, box_x
        dimension = "3D"
        if two_2:
            dimension = "2D"
        if index is not None:
            index = "x" + str(index)
        else:
            index = ""
        return f"{pal_x}x{pal_y}x{box_x}x{box_y}{index}x{dimension}"

    def export_to_json(self, *, pallet_index: str = "001", weight: float = 0) -> dict:
        art = {
            "0": {
                "description": "SingleItem",
                "weight": weight if weight > 0 else 1,
                "shippingGroup": "A",
            }}
        pal = [
            {
                "palletNr": pallet_index,
                "palletType": self.__pallet_type,
                "palletDimension": {
                    "x": self.__x,
                    "y": self.__y
                },
                "boxes": [box.export_to_json() for box in self.__boxes]
            }
        ]
        return {
            "pallets": pal,
            "articles": art,
            "orderID": ""
        }


class Pallet2D_Frame(tk.Frame):
    def __init__(self, parent, enable: bool = True) -> None:
        tk.Frame.__init__(self, parent)
        self.pallet_sim = Pallet_Sim()
        self.mujoco_viewer = None
        self.pybullet_viewer = None
        self.__enabled = None
        self.pallets = []
        self.parent = parent

        # add a menu bar with the option to save the pallets or view in simulation mode mujoco or pybullet can be selected
        self.pallet_viewer_menu_bar = tk.Menu(self)
        # make a save sub menu with the option to save the current pallet or all pallets
        self.save_menu = tk.Menu(self.pallet_viewer_menu_bar, tearoff=0)
        self.save_menu.add_command(label="Save current pallet", command=self.save_current_pallet)
        self.save_menu.add_command(label="Save all as order", command=self.save_all_pallets)
        self.pallet_viewer_menu_bar.add_cascade(label="Save", menu=self.save_menu)
        # a submenu for the view options (mujoco or pybullet)
        self.view_menu = tk.Menu(self.pallet_viewer_menu_bar, tearoff=0)
        self.view_menu.add_command(label="Mujoco",
                                   command=lambda sim_engine="mujoco": self.show_in_simulation(sim_engine))
        self.view_menu.add_command(label="Pybullet",
                                   command=lambda sim_engine="pybullet": self.show_in_simulation(sim_engine))
        self.pallet_viewer_menu_bar.add_cascade(label="View", menu=self.view_menu)
        # add back the menu bar to the parent
        self.pallet_viewer_menu_bar.add_command(label="Back", command=self.back_button)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self)
        self.left_button = tk.Button(self.button_frame, text="<",
                                     command=lambda direction="left": self.change_image(direction))
        self.right_button = tk.Button(self.button_frame, text=">",
                                      command=lambda direction="right": self.change_image(direction))

        self.left_button.pack(side=tk.LEFT)
        self.right_button.pack(side=tk.LEFT)
        self.button_frame.pack(side=tk.BOTTOM)

        self.index = 0
        # listen for left and right arrow keys to scroll through the layouts
        self.parent.bind("<Left>", lambda event, direction="left": self.change_image(direction))
        self.parent.bind("<Right>", lambda event, direction="right": self.change_image(direction))
        # attach the resize event to the frame
        self.parent.bind("<Configure>", lambda _: self.on_resize())
        self.back_button_callback = None
        self.enable(enable)

    def save_all_pallets(self):
        if not self.__enabled:
            return
        # open a file dialog to select the directory to save the pallet in
        # the name of the 2 files is WxLxIndexx2D and WxLxIndexx3D in mm
        # there are 2 files one for the pallet and one for the articles (.pal.json and .art.json)
        file_path = filedialog.askdirectory(title="Select directory to save the order", initialdir=".")
        if file_path == "":
            return

        # pal_x, pal_y = self.pallets[self.index].get_x(), self.pallets[self.index].get_y()
        # box_x, box_y = self.pallets[self.index][0].get_dim_x(), self.pallets[self.index][0].get_dim_y()
        # if pal_x < pal_y:
        #     pal_x, pal_y = pal_y, pal_x
        # name = f"{pal_x}x{pal_y}x{box_x}x{box_y}x2D"
        # check if the pallet is already saved in the directory and if so ask is it should be overwritten or not
        name = self.pallets[self.index].get_name()
        if os.path.isfile(f"{file_path}/{name}.order.json"):
            overwrite = messagebox.askyesno("Overwrite", "Order already exists, overwrite?")
            if not overwrite:
                return
        pals = []
        art = {}
        for i, pallet in enumerate(self.pallets):
            order = pallet.export_to_json(pallet_index=str(i + 1).zfill(3))
            pal, art = order["pallets"], order["articles"]
            pals.extend(pal)
        # remake order json
        order = {
            "pallets": pals,
            "articles": art,
            "orderID": ""
        }
        # save the .order.json file
        with open(f"{file_path}/{name}.order.json", "w") as f:
            json.dump(order, f, indent=4)
        # show a popup to inform the user that the pallet was saved
        messagebox.showinfo("Saved", "Order saved")

    def save_current_pallet(self):
        if not self.__enabled:
            return
        # open a file dialog to select the directory to save the pallet in
        # the name of the 2 files is W x L x Box_x x Box_y x x Index x 2D
        # there are 2 files one for the pallet and one for the articles (.pal.json and .art.json)
        file_path = filedialog.askdirectory(title="Select directory to save pallet", initialdir=".")
        if file_path == "":
            return
        # name = f"{self.pallets[self.index].get_x()}x{self.pallets[self.index].get_y()}" \
        #        f"x{self.pallets[self.index][0].get_dim_x()}x{self.pallets[self.index][0].get_dim_y()}" \
        #        f"x{self.index}x2D"

        name = self.pallets[self.index].get_name(index=self.index)
        # check if the pallet is already saved in the directory and if so ask is it should be overwritten or not
        if os.path.isfile(f"{file_path}/{name}.order.json"):
            overwrite = messagebox.askyesno("Overwrite", "Pallet already exists, overwrite?")
            if not overwrite:
                return
        order = self.pallets[self.index].export_to_json()
        # save the .order.json file
        with open(f"{file_path}/{name}.order.json", "w") as f:
            json.dump(order, f, indent=4)
        # show a popup to inform the user that the pallet was saved
        messagebox.showinfo("Saved", "Pallet saved")

    def back_button(self) -> None:
        if self.mujoco_viewer is not None:
            self.mujoco_viewer.close()
        if self.pybullet_viewer is not None:
            self.pybullet_viewer.close()
        if self.back_button_callback is not None:
            self.back_button_callback()

    def show_in_simulation(self, sim_engine: str) -> None:
        if not self.__enabled:
            return
        self.pallet_sim.load(json_data=self.pallets[self.index].export_to_json())
        if sim_engine == "mujoco":
            if self.mujoco_viewer is not None:
                self.mujoco_viewer.close()
            self.mujoco_viewer = Pallet_Sim.MujocoProjectViewer(self.pallet_sim.export_pallet(0, "mujoco"))
        elif sim_engine == "pybullet":
            if self.pybullet_viewer is not None:
                self.pybullet_viewer.close()
            self.pybullet_viewer = Pallet_Sim.PyBulletProjectViewer(self.pallet_sim.export_pallet(0, "pybullet"))

    def draw(self) -> None:
        self.canvas.delete("all")
        # offset_y = 25
        if len(self.pallets) > 0:
            pallet = self.pallets[self.index]
            pallet_width = pallet.get_x()
            pallet_length = pallet.get_y()
            multy = min((self.parent.winfo_height() - 25) / pallet_length,
                        self.parent.winfo_width() / pallet_width) * 0.9
            offset_x = self.parent.winfo_width() / 2 - pallet_width * multy / 2
            offset_y = (self.parent.winfo_height() - 5) / 2 - pallet_length * multy / 2

            for box in pallet:
                x, y, _, x1, y1, _ = box.get_coordinates()
                x = x * multy + offset_x
                y = y * multy + offset_y
                x1 = x1 * multy + offset_x
                y1 = y1 * multy + offset_y
                # make all x and y values ints
                x, y, x1, y1 = int(x), int(y), int(x1), int(y1)
                self.canvas.create_rectangle(x, y, x1, y1, fill="blue", outline="white", width=2)

            self.canvas.create_rectangle(0 + offset_x, 0 + offset_y, int(pallet_width * multy + offset_x),
                                         int(pallet_length * multy + offset_y), width=5, outline="black")

            # draw the index and the total number of layouts in the top center of the canvas
            self.canvas.create_text(self.parent.winfo_width() / 2, 20, font="Arial 15",
                                    text="Layout {}/{} boxes ({})".format(self.index + 1, len(self.pallets),
                                                                          len(pallet)))
        else:
            # print at the center of the canvas that there are no pallets
            self.canvas.create_text(self.parent.winfo_width() / 2, self.parent.winfo_height() / 2,
                                    font="Arial 20", text="No pallets")

    def on_resize(self):
        if not self.__enabled:
            return
        self.draw()

    def change_image(self, direction):
        if not self.__enabled:
            return
        if direction == "left":
            if self.index > 0:
                self.index -= 1
                if self.index == 0:
                    self.left_button.config(state=tk.DISABLED)
                self.draw()
                if self.index < len(self.pallets) - 1:
                    self.right_button.config(state=tk.NORMAL)
        elif direction == "right":
            if self.index < len(self.pallets) - 1:
                self.index += 1
                if self.index == len(self.pallets) - 1:
                    self.right_button.config(state=tk.DISABLED)
                self.draw()
                if self.index > 0:
                    self.left_button.config(state=tk.NORMAL)

    def enable(self, value: bool):
        if value:
            self.parent.config(menu=self.pallet_viewer_menu_bar)
        self.__enabled = value

    def set_pallets(self, pallets):
        self.pallets = pallets
        self.index = 0
        self.left_button.config(state=tk.DISABLED)
        self.right_button.config(state=tk.DISABLED)
        for i in range(2):
            self.pallet_viewer_menu_bar.entryconfig(i + 1, state=tk.DISABLED)
        if len(self.pallets) != 0:
            for i in range(2):
                self.pallet_viewer_menu_bar.entryconfig(i + 1, state=tk.NORMAL)
        if len(self.pallets) > 1:
            self.right_button.config(state=tk.NORMAL)
        self.draw()


class InputFrame(tk.Frame):
    def __init__(self, parent, enable: bool = True):
        tk.Frame.__init__(self, parent)
        self.using_3d = False
        self.font = ("Arial", 15)
        self.pallets = []
        self.__enabled = None
        self.start_callback = None
        self.back_button_callback = None
        self.parent = parent

        # make a menu bar with a start button and a back button
        self.input_menu_bar = tk.Menu(self)
        self.input_menu_bar.add_command(label="Start", command=self.start, font=self.font)
        self.input_menu_bar.add_command(label="Back", font=self.font,
                                        command=lambda: self.back_button_callback() if self.back_button_callback is not None else tk.messagebox.showerror(
                                            "Error", "No back button callback set"))

        pad_dic = {"padx": 10, "pady": 15}

        # create a frame for the pallet size input
        self.pallet_frame = tk.LabelFrame(self, text="Pallet size (mm)", font=self.font)
        self.pallet_frame.pack(side=tk.TOP, fill=tk.X, **pad_dic)

        # add the option to select from a list of pallets (Euro (1200x800) or Dusseldorfer (600x800)
        # or the option to enter custom pallet sizes (width and length))

        self.known_pallet_types = {
            "Euro": (800, 1200),
            "Duesseldorfer": (600, 800),
            "Custom": None
        }

        self.pallet_type_var = tk.StringVar()
        self.pallet_type_option_menu = tk.OptionMenu(self.pallet_frame, self.pallet_type_var,
                                                     *self.known_pallet_types.keys(),
                                                     command=self.on_pallet_size_option_menu_change)
        self.pallet_type_option_menu.config(font=self.font)
        self.pallet_type_option_menu.pack(side=tk.LEFT, **pad_dic)

        # create a frame for the box size input
        self.box_frame = tk.LabelFrame(self, text="Box size (mm)", font=self.font)
        self.box_frame.pack(side=tk.TOP, fill=tk.X, **pad_dic)

        self.label_pallet_width = tk.Label(self.pallet_frame, text="Width", font=self.font)
        self.label_pallet_width.pack(side=tk.LEFT, **pad_dic)
        self.pallet_x_input = tk.Entry(self.pallet_frame, font=self.font, width=5)
        self.pallet_x_input.pack(side=tk.LEFT, **pad_dic)

        self.label_pallet_length = tk.Label(self.pallet_frame, text="Length", font=self.font)
        self.label_pallet_length.pack(side=tk.LEFT, **pad_dic)
        self.pallet_y_input = tk.Entry(self.pallet_frame, font=self.font, width=5)
        self.pallet_y_input.pack(side=tk.LEFT, **pad_dic)

        self.label_box_width = tk.Label(self.box_frame, text="Width", font=self.font)
        self.label_box_width.pack(side=tk.LEFT, **pad_dic)
        self.box_x_input = tk.Entry(self.box_frame, font=self.font, width=5)
        self.box_x_input.pack(side=tk.LEFT, **pad_dic)

        self.label_box_length = tk.Label(self.box_frame, text="Length", font=self.font)
        self.label_box_length.pack(side=tk.LEFT, **pad_dic)
        self.box_y_input = tk.Entry(self.box_frame, font=self.font, width=5)
        self.box_y_input.pack(side=tk.LEFT, **pad_dic)

        self.label_box_height = tk.Label(self.box_frame, text="Height", font=self.font)
        self.label_box_height.pack(side=tk.LEFT, **pad_dic)
        self.box_z_input = tk.Entry(self.box_frame, font=self.font, width=5)
        self.box_z_input.pack(side=tk.LEFT, **pad_dic)

        self.clean_inputs()
        self.enable(enable)

    def on_pallet_size_option_menu_change(self, value):
        self.pallet_x_input.config(state=tk.NORMAL)
        self.pallet_y_input.config(state=tk.NORMAL)
        if value != "Custom":
            self.pallet_x_input.delete(0, tk.END)
            self.pallet_y_input.delete(0, tk.END)
            self.pallet_x_input.insert(0, self.known_pallet_types[value][0])
            self.pallet_y_input.insert(0, self.known_pallet_types[value][1])
            self.pallet_x_input.config(state=tk.DISABLED)
            self.pallet_y_input.config(state=tk.DISABLED)

    def set_dimensions(self, using_3d: bool = False):
        self.using_3d = using_3d
        # if not using 3d, remove the z input and rename the labels
        if not self.using_3d:
            self.box_z_input.pack_forget()
            self.label_box_height.pack_forget()
        else:
            self.box_z_input.pack(side=tk.LEFT, pady=15, padx=10)
            self.box_z_input.pack(side=tk.LEFT, pady=15, padx=10)
        self.clean_inputs()

    def clean_inputs(self):
        fs_pallet = self.known_pallet_types.keys().__iter__().__next__()
        self.pallet_type_var.set(fs_pallet)
        self.on_pallet_size_option_menu_change(fs_pallet)
        self.box_x_input.delete(0, tk.END)
        self.box_y_input.delete(0, tk.END)
        self.box_z_input.delete(0, tk.END)

    def start(self):
        for i in range(2):
            self.input_menu_bar.entryconfig(i + 1, state=tk.DISABLED)

        # get the pallet size from the input
        pallet_x = self.pallet_x_input.get().strip()
        pallet_y = self.pallet_y_input.get().strip()
        # get the box size from the input
        box_x = self.box_x_input.get().strip()
        box_y = self.box_y_input.get().strip()
        if self.using_3d:
            box_z = self.box_z_input.get().strip()
        else:
            box_z = "0"

        # disable input fields
        self.pallet_x_input.config(state=tk.DISABLED)
        self.pallet_y_input.config(state=tk.DISABLED)
        self.box_x_input.config(state=tk.DISABLED)
        self.box_y_input.config(state=tk.DISABLED)
        self.box_z_input.config(state=tk.DISABLED)
        self.pallet_type_option_menu.config(state=tk.DISABLED)

        # check if the input is valid
        if pallet_x == "" or pallet_y == "" or box_x == "" or box_y == "" or box_z == "":
            messagebox.showerror("Error", "Please fill in all the fields")
        elif not pallet_x.isdigit() or not pallet_y.isdigit() or not box_x.isdigit() or not box_y.isdigit() or not box_z.isdigit():
            messagebox.showerror("Error", "Please enter only numbers")
        else:
            self.pallets = []
            # make box and pallet data ints
            pallet_x = int(pallet_x)
            pallet_y = int(pallet_y)
            box_x = int(box_x)
            box_y = int(box_y)
            box_z = int(box_z)

            # # make sure y > x if not flip them and print a warning
            # message = ""
            # if pallet_y < pallet_x:
            #     message += "Pallet length is smaller than width, flipping them\n"
            #     pallet_x, pallet_y = pallet_y, pallet_x
            # if box_y < box_x:
            #     message += "Box length is smaller than width, flipping them\n"
            #     box_x, box_y = box_y, box_x
            # if message != "":
            #     messagebox.showwarning("Warning", message)
            #     print(message)

            try:
                res = algorithm_artikel(box_x, box_y, box_z, pallet_x, pallet_y, True)
                # flip tuple res["pallets_size"]
                pallets = res["pallets"]
                for boxes_pos, box_size in pallets:
                    # for lst_box, bxsz in algorithm_artikel(box_x, box_y, box_z, pallet_x, pallet_y):
                    pallet = Pallet2D_Handler(res["pallet_size"], self.pallet_type_var.get() + "_Pallet")
                    for box, sz in zip(boxes_pos, box_size):
                        pallet.add(box, sz)
                    if len(pallet) > 0:
                        self.pallets.append(pallet)
                    else:
                        print("Warning: Pallet is empty")
                    # self.update()

                if len(self.pallets) == 0:
                    messagebox.showerror("Error", "No layouts where generated")
                elif self.start_callback is not None:
                    self.start_callback()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                print(e)

        for i in range(2):
            self.input_menu_bar.entryconfig(i + 1, state=tk.NORMAL)

        self.box_x_input.config(state=tk.NORMAL)
        self.box_y_input.config(state=tk.NORMAL)
        self.box_z_input.config(state=tk.NORMAL)
        self.pallet_type_option_menu.config(state=tk.NORMAL)
        self.on_pallet_size_option_menu_change(self.pallet_type_var.get())

    def enable(self, value: bool):
        self.__enabled = value
        if value:
            self.parent.config(menu=self.input_menu_bar)


class Simulation_Viewer_Frame(tk.Frame):
    def __init__(self, parent, enable: bool = True):
        super().__init__(parent)

        self.path_data = None
        self.json_data = None

        self.__enabled = None
        self.parent = parent
        bg_color = "#6D6D6D"

        self.configure(bg=bg_color)
        self.font = ("Arial", 15)
        self.mujoco_project_viewer = None
        self.pybullet_project_viewer = None
        self.images = []
        self.color_by = "product_code"
        self.last_results = None

        self.canvas_frame = tk.Frame(self, width=1500, height=650)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.h = tk.Scrollbar(self, orient='horizontal')
        self.h.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.canvas_frame, width=1500, height=650, xscrollcommand=self.h.set,
                                background=bg_color, highlightthickness=0, bd=0)
        self.canvas.pack(side=tk.TOP, fill=tk.X)

        # function call for when canvas is double-clicked
        self.canvas.bind("<Double-Button-1>", self.canvas_double_click)

        self.h.config(command=self.canvas.xview)

        # add 2 sliders to control the pallets simulation parameters and add a label on top saying "Force"
        self.slider_frame = tk.Frame(self, width=1500, height=150, bg=bg_color, highlightthickness=0, bd=0)
        self.slider_frame.pack(side=tk.TOP, fill=tk.X)

        # self.label_force = tk.Label(self.slider_frame, text="Force", font=("Arial", 18), bg=bg_color, fg="white")
        # self.label_force.pack(side=tk.TOP)

        from_, to, resolution = 0.0, 0.7, 0.01

        self.label_force_x = tk.Label(self.slider_frame, text="X", font=self.font, bg=bg_color, fg="white")
        self.label_force_x.pack(side=tk.TOP, fill=tk.X)
        self.slider_x = tk.Scale(self.slider_frame, from_=from_, to=to, resolution=resolution, font=self.font,
                                 bg=bg_color, fg="white", orient=tk.HORIZONTAL, length=500, showvalue=False,
                                 command=lambda x: self.label_force_x.config(text=f"Force X: {x}"))
        self.slider_x.pack(side=tk.TOP)

        self.label_force_y = tk.Label(self.slider_frame, text="Y", font=self.font, bg=bg_color, fg="white")
        self.label_force_y.pack(side=tk.TOP, fill=tk.X)
        self.slider_y = tk.Scale(self.slider_frame, from_=from_, to=to, resolution=resolution, font=self.font,
                                 bg=bg_color, fg="white", orient=tk.HORIZONTAL, length=500, showvalue=False,
                                 command=lambda y: self.label_force_y.config(text=f"Force Y: {y}"))
        self.slider_y.pack(side=tk.TOP)

        # add the default values to the sliders .3 to all
        self.slider_x.set(0.35)
        self.slider_y.set(0.35)

        self.label_fps = tk.Label(self.slider_frame, text="Fps", font=self.font, bg=bg_color, fg="white")
        self.label_fps.pack(side=tk.TOP, fill=tk.X)
        self.slider_fps = tk.Scale(self.slider_frame, from_=1, to=120, resolution=1, font=self.font,
                                   bg=bg_color, fg="white", orient=tk.HORIZONTAL, length=500, showvalue=False,
                                   command=lambda fps: self.label_fps.config(text=f"FPS: {fps}"))
        self.slider_fps.pack(side=tk.TOP)
        self.slider_fps.set(60)

        self.pallet_sim = Pallet_Sim(img_callback=self.update_images, loop_callback=self.loop_callback)
        self.thread_pallets, self.thread_tests = True, True
        self.sim_engine = "mujoco"

        # make a menu bar with a simulation menu to run or load a simulation
        self.sim_menu_bar = tk.Menu(self)
        self.sim_menu = tk.Menu(self.sim_menu_bar, tearoff=0)

        self.sub_menu_simulate = tk.Menu(self.sim_menu, tearoff=0)
        self.sim_menu.add_cascade(label="Simulate", menu=self.sub_menu_simulate)
        self.sub_menu_simulate_headless = tk.Menu(self.sim_menu, tearoff=0)
        self.sim_menu.add_cascade(label="Simulate Headless", menu=self.sub_menu_simulate_headless)
        self.sim_menu_bar.add_cascade(label="Simulation", menu=self.sim_menu)

        self.load_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.load_menu.add_command(label="Load from Proprietary XML",
                                   command=lambda method="xml": self.load_simulation(method))
        self.load_menu.add_command(label="Load from Generic JSON",
                                   command=lambda method="json": self.load_simulation(method))
        self.sim_menu_bar.add_cascade(label="Load", menu=self.load_menu)

        # add a menu for selecting which type of color_by to use when displaying pallets and a tick for the one
        # currently selected
        self.color_by_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.color_by_menu.add_command(
            label="✓ Product Code",
            command=lambda option="product_code", index=0: self.set_color_by_option(option, index))
        self.color_by_menu.add_command(
            label="Shipping Group",
            command=lambda option="shipping_group", index=1: self.set_color_by_option(option, index))
        self.color_by_menu.add_command(
            label="Weight", command=lambda option="weight", index=2: self.set_color_by_option(option, index))
        self.sim_menu_bar.add_cascade(label="Color By", menu=self.color_by_menu)

        # add a menu for selecting if the test or pallets should be threaded and a tick if it's currently active or not
        self.threading_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.threading_menu.add_command(
            label="✓ Test", command=lambda option="test", index=0: self.set_threading_option(option, index))
        self.threading_menu.add_command(
            label="✓ Pallets", command=lambda option="pallets", index=1: self.set_threading_option(option, index))
        self.sim_menu_bar.add_cascade(label="Threading", menu=self.threading_menu)

        # add a menu for selecting the simulation engine to use (mujoco or pybullet)
        self.engine_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.engine_menu.add_command(
            label="✓ Mujoco", command=lambda option="mujoco", index=0: self.set_engine_option(option, index))
        self.engine_menu.add_command(
            label="PyBullet", command=lambda option="pybullet", index=1: self.set_engine_option(option, index))
        self.sim_menu_bar.add_cascade(label="Simulation Engine", menu=self.engine_menu)

        # add a menu for selecting the option to generate a new pallet, under the option to be 2D or 3D
        self.generate_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.generate_menu.add_command(
            label="2D", command=lambda index=0: self.set_generate_option(index))
        self.generate_menu.add_command(
            label="3D", command=lambda index=1: self.set_generate_option(index))
        self.sim_menu_bar.add_cascade(label="Generate Pallet", menu=self.generate_menu)

        # add a "help" menu that opens a new window with the help text
        self.help_menu = tk.Menu(self.sim_menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.open_help_window)
        self.sim_menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # add close button to the menu bar
        self.sim_menu_bar.add_command(label="Close", command=self.close_window)
        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)
        self.generate_pallet_callback = None
        self.enable(enable)

    def open_help_window(self):
        HELP_TEXT = """
        This is a simple GUI for the pallet_sim package. It allows you to run simulations of pallets and tests and
        visualise the results.
        """
        # show a popup window with the help text
        help_window = tk.Toplevel(self.parent)
        help_window.title("Help")
        help_window.geometry("800x600")
        help_window.resizable(False, False)
        help_window.grab_set()
        help_window.focus_set()
        help_window.transient(self.parent)
        help_window.protocol("WM_DELETE_WINDOW", lambda: help_window.destroy())
        help_text = tk.Text(help_window, wrap="word")
        help_text.pack(fill="both", expand=True)
        help_text.insert("1.0", HELP_TEXT)
        help_text.config(state="disabled")

    def set_generate_option(self, index):
        # if index not 0 show a message box to say that 3D pallets are not yet supported
        if index != 0:
            messagebox.showinfo("Info", "3D pallets are not yet supported")
            return
        if self.generate_pallet_callback is not None:
            self.generate_pallet_callback()

    def enable_menus(self, state) -> None:
        self.config(cursor="watch" if state == "disabled" else "")
        for i in range(6):
            self.sim_menu_bar.entryconfig(i + 1, state=state)
        # disable sliders when running a simulation
        self.slider_y.config(state=state)
        self.slider_x.config(state=state)
        # change the double click event in from the canvas
        self.canvas.bind("<Double-Button-1>", self.canvas_double_click if state == "normal" else "")
        # change the state of the fps slider, x and y sliders
        self.slider_fps.config(state=state)
        self.slider_x.config(state=state)
        self.slider_y.config(state=state)

    def set_engine_option(self, option: str, index: int) -> None:
        for i in range(self.engine_menu.index(tk.END) + 1):
            self.engine_menu.entryconfig(i, label=self.engine_menu.entrycget(i, "label").replace("✓ ", ""))
        # check the option that was selected by adding a ✓ to the start of the label string
        self.engine_menu.entryconfig(index, label=f"✓ {self.engine_menu.entrycget(index, 'label')}")
        self.sim_engine = option

    def set_threading_option(self, option: str, index: int) -> None:
        # set the threading option to the one selected and update the menu
        if option == "test":
            self.thread_tests = not self.thread_tests
            self.threading_menu.entryconfig(
                index, label=f"✓ {option.title()}" if self.thread_tests else option.title())
        elif option == "pallets":
            self.thread_pallets = not self.thread_pallets
            self.threading_menu.entryconfig(
                index, label=f"✓ {option.title()}" if self.thread_pallets else option.title())

    def set_color_by_option(self, option: str, index: int) -> None:
        # and uncheck the other options
        for i in range(self.color_by_menu.index(tk.END) + 1):
            self.color_by_menu.entryconfig(i, label=self.color_by_menu.entrycget(i, "label").replace("✓ ", ""))
        # check the option that was selected by adding a ✓ to the start of the label string
        self.color_by_menu.entryconfig(index, label=f"✓ {self.color_by_menu.entrycget(index, 'label')}")
        self.color_by = option
        self.display_pallets(results=self.last_results)

    def canvas_double_click(self, event: tk.Event) -> None:
        # when the canvas is double-clicked, center the view on the pallet that was clicked

        # add the scroll offset to the click position
        event.x += self.canvas.xview()[0] * self.canvas.winfo_width()
        for i, image in enumerate(self.images):
            # using the image bounding box, check if the click was inside the image
            height = image.height() * 3 / 4
            width = image.width() * (i + 1)
            if width > event.x > width - image.width() and height > event.y > 0:
                if self.sim_engine == "mujoco":
                    if self.mujoco_project_viewer is not None:
                        self.mujoco_project_viewer.close()
                    self.mujoco_project_viewer = Pallet_Sim.MujocoProjectViewer(
                        self.pallet_sim.export_pallet(i, "mujoco"))
                else:
                    if self.pybullet_project_viewer is not None:
                        self.pybullet_project_viewer.close()

                    self.pybullet_project_viewer = Pallet_Sim.PyBulletProjectViewer(
                        self.pallet_sim.export_pallet(i, "pybullet"))
                break

    def run_simulation(self, display: bool = True, pallet: str = "all") -> None:
        def create_test() -> list:
            def create_step(test_time: float, force_x: float, force_y: float, period: float = 0.1) -> dict:
                return {
                    "time": test_time,
                    "force_x": force_x,
                    "force_y": force_y,
                    "period": period,
                }

            return [
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
                        create_step(5, self.slider_x.get(), 0),
                        create_step(10, -self.slider_x.get(), 0)
                    ]
                },
                {
                    "name": "Y axis",
                    "duration": 50,
                    "steps": [
                        create_step(5, 0, self.slider_y.get()),
                        create_step(10, 0, -self.slider_y.get())
                    ]
                }
            ]

        if self.mujoco_project_viewer is not None:
            self.mujoco_project_viewer.close()
            self.mujoco_project_viewer = None

        if self.pybullet_project_viewer is not None:
            self.pybullet_project_viewer.close()
            self.pybullet_project_viewer = None

        self.display_pallets()
        self.canvas.config(scrollregion=(0, 0, 1500, 650))

        self.enable_menus("disabled")
        self.pallet_sim.tests = create_test()

        now = time.time()
        results = self.pallet_sim.run_simulation(simulation_engine=self.sim_engine,
                                                 pallet_nr=pallet,
                                                 view=display,
                                                 thread_tests=self.thread_tests,
                                                 thread_pallets=self.thread_pallets,
                                                 fps=int(self.slider_fps.get()),
                                                 color_by=self.color_by)

        print(f"Simulation took {time.time() - now:.1f} seconds using {self.sim_engine} engine")

        self.display_pallets(results)
        self.parent.title(f"Simulation Viewer  Order {self.pallet_sim.get_order_id()} completed")

        # enable the menu bar
        self.enable_menus("normal")

    def load_simulation(self, method: str = "xml") -> None:
        def load():
            if file:
                status = False
                if method == "xml":
                    status = self.pallet_sim.load(path_data=file)
                    self.path_data = file
                elif method == "json":
                    with open(file) as f:
                        json_data = f.read()
                    status = self.pallet_sim.load(json_data=json_data)
                    self.json_data = json_data
                if status:
                    self.last_results = None
                    self.display_pallets()

                    self.parent.title(f"Simulation Viewer  Order {self.pallet_sim.get_order_id()} loaded")
                    # clear ths sub menu and add a new command for each pallet in the order

                    self.sub_menu_simulate.add_command(label=f"All", command=lambda: self.run_simulation(True))
                    self.sub_menu_simulate_headless.add_command(label=f"All",
                                                                command=lambda: self.run_simulation(False))

                    for pallet_id in self.pallet_sim.get_pallet_nrs():
                        self.sub_menu_simulate.add_command(
                            label=f"{pallet_id}",
                            command=lambda p=pallet_id: self.run_simulation(pallet=p)
                        )
                        self.sub_menu_simulate_headless.add_command(
                            label=f"{pallet_id}",
                            command=lambda p=pallet_id: self.run_simulation(display=False, pallet=p)
                        )

                else:
                    self.path_data = None
                    self.json_data = None
                    self.parent.title("Simulation Viewer  Error loading order")
                    # clear canvas
                    self.canvas.delete("all")

        self.enable_menus("disabled")

        self.parent.title("Simulation Viewer loading...")
        self.sub_menu_simulate.delete(0, tk.END)
        self.sub_menu_simulate_headless.delete(0, tk.END)
        self.last_results = None
        self.images = []
        self.canvas.delete("all")
        self.update()

        initial_dir=pkg_resources.resource_filename(__name__, "examples")

        # open a file dialog to select a simulation file
        if method == "xml":
            file = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("xml files", ["*.pal.xml"]), ("all files", "*.*")),
                                              initialdir=initial_dir)
        else:
            file = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("json files", ["*.order.json"]), ("all files", "*.*")),
                                              initialdir=initial_dir)

        load_thread = threading.Thread(target=load, daemon=True)
        load_thread.start()
        while load_thread.is_alive():
            self.update()
            time.sleep(.2)

        self.enable_menus("normal")

    def loop_callback(self, info: dict) -> None:
        self.update()
        self.parent.title((", ".join([f"{k.capitalize()}: {v}" for k, v in info.items()])))

    def update_images(self, imgs: dict) -> None:
        self.images = []
        width, height = imgs["width"], imgs["height"]
        self.canvas.delete("all")

        for i, img_code in enumerate(["fixed", "corner", "top"]):
            img = Image.fromarray(imgs["imgs"][img_code])
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(i * width, 0, anchor=tk.NW, image=img)
            # add a label to the images in the center of each image with a big font
            self.canvas.create_text(i * width + width / 2, height - 10, text=img_code, font=self.font, fill="white")
            self.images.append(img)
        self.canvas.update()

    def display_pallets(self, results: dict = None) -> None:
        self.enable_menus("disabled")

        self.last_results = results

        self.images = []
        self.canvas.delete("all")

        pallets_images = self.pallet_sim.get_order_images()
        height = pallets_images["height"]
        width = pallets_images["width"]

        self.canvas.config(scrollregion=(0, 0, width * len(pallets_images["pallets"]), height))

        for pallet in pallets_images["pallets"]:
            index = pallet["index"]

            img = Image.fromarray(pallet["images"][self.color_by])
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(index * width, 0, anchor=tk.NW, image=img)
            # add a label to the images in the center of each image with a big font
            self.canvas.create_text(index * width + width / 2, 25, text=pallet["palletNr"], font=self.font,
                                    fill="white")
            # display the amount of boxes in the image located in order.pallets if i == 0 the print box in the left
            # corner
            self.canvas.create_text(index * width + width / 2, height // 3 * 2 - 10, text=f"{pallet['boxes']}",
                                    font=self.font, fill="white")
            self.images.append(img)

        self.canvas.create_text(40, (height // 3 * 2) - 10, text=f"Boxes", font=self.font, fill="white")

        if results is not None:
            # bellow the images display the results of the simulation of each test with the name of the test
            number_tests = len(results["testsNames"])
            for j, test_name in enumerate(results["testsNames"]):
                self.canvas.create_text(40, (height // 3 * 2 + 25 * j) + 20, text=f"{test_name}", font=self.font,
                                        fill="white")
            self.canvas.create_text(40, (height // 3 * 2 + 25 * number_tests) + 30, text=f"Results:", font=self.font,
                                    fill="white")

            for pallets in results["pallets"]:
                index = pallets["index"]
                for k, testResult in enumerate(pallets["testResults"]):
                    color = "blue" if testResult else "red"
                    text = "Pass" if testResult else "Fail"
                    self.canvas.create_text(index * width + width / 2, (height // 3 * 2 + 25 * k) + 20,
                                            text=f"{text}", font=self.font, fill=f"{color}")
                # display the total number of tests passed and failed if 100% passed display in blue color 0%
                # passed display in red  if anything else display in orange along with the percentage

                passed = sum(pallets["testResults"])
                text = "Pass" if passed == number_tests else "Fail" if passed == 0 else f"{passed}/{number_tests}"
                color = "blue" if passed == number_tests else "red" if passed == 0 else "orange"
                self.canvas.create_text(index * width + width / 2, (height // 3 * 2 + 25 * number_tests) + 30,
                                        text=text, font=self.font, fill=color)
        self.canvas.update()
        self.enable_menus("normal")

    def close_window(self) -> None:
        self.destroy()
        self.quit()

    def enable(self, value: bool):
        self.__enabled = value
        if value:
            self.parent.config(menu=self.sim_menu_bar)
        else:
            if self.pybullet_project_viewer is not None:
                self.pybullet_project_viewer.close()
            if self.mujoco_project_viewer is not None:
                self.mujoco_project_viewer.close()


class main_window(tk.Tk):
    def __init__(self):
        super().__init__()

        def switch_to_pallets():
            input_frame.pack_forget()
            pallet2d_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            input_frame.enable(False)
            pallet2d_frame.enable(True)
            pallet2d_frame.set_pallets(input_frame.pallets)

        def switch_to_input():
            pallet2d_frame.pack_forget()
            input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            input_frame.enable(True)
            pallet2d_frame.enable(False)

        def from_sim_to_input():
            simulation_frame.pack_forget()
            input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            input_frame.enable(True)
            input_frame.set_dimensions()
            simulation_frame.enable(False)

        def switch_to_sim():
            input_frame.pack_forget()
            simulation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            input_frame.enable(False)
            simulation_frame.enable(True)

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.title("Simulation Viewer")
        self.state("zoomed")
        self.resizable(True, True)

        input_frame = InputFrame(self, False)
        # input_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        input_frame.start_callback = switch_to_pallets
        input_frame.back_button_callback = switch_to_sim

        pallet2d_frame = Pallet2D_Frame(self, False)
        pallet2d_frame.back_button_callback = switch_to_input

        simulation_frame = Simulation_Viewer_Frame(self, True)
        simulation_frame.generate_pallet_callback = from_sim_to_input
        simulation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def main():
    main_window().mainloop()


if __name__ == "__main__":
    main()
