import pkg_resources

import pyvista
import numpy as np

# for use in jupyter notebook use
# pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'
try:
    pyvista.set_jupyter_backend('client')
except ImportError as e:
    print(e)


def _make_box(anchor: dict[str], dimension: dict[str]):
    anchor = (anchor["x"], anchor["y"], anchor["z"])
    dimension = (dimension["x"], dimension["y"], dimension["z"])
    x = np.linspace(anchor[0], anchor[0] + dimension[0], 25)
    y = np.linspace(anchor[1], anchor[1] + dimension[1], 25)
    z = np.linspace(anchor[2], anchor[2] + dimension[2], 25)
    grid = pyvista.StructuredGrid(*np.meshgrid(x, y, z))
    surf = grid.extract_surface().triangulate()
    surf.flip_normals()
    return surf


def show_pallet(pallet: dict, dark_mode: bool = False):
    p = pyvista.Plotter()
    pal_anchor = {"x": 0, "y": 0, "z": -144}
    pal_dimension = {"x": pallet["palletDimension"]["x"], "y": pallet["palletDimension"]["y"], "z": 144}
    p.add_mesh(_make_box(pal_anchor, pal_dimension), color='brown', smooth_shading=True, split_sharp_edges=True)
    for box in pallet["boxes"]:
        p.add_mesh(_make_box(box["anchor"], box["dimension"]), color=np.random.rand(3, ), smooth_shading=True,
                   split_sharp_edges=True)
    # change the background color to white
    p.set_background('black' if dark_mode else 'white')
    p.show()


def main():
    # from order import Order
    # from threading import Thread
    # order = Order(json_data=open(r'./obfuscated_output/0615610.order.json').read())
    # Thread(target=show_pallet, args=(order.get_pallet(0), False)).start()
    # Thread(target=show_pallet, args=(order.get_pallet(0), True)).start()
    from .pallet_sim import Pallet_Sim
    import time
    pallet_sim = Pallet_Sim()
    pallet_sim.load(json_data=open(pkg_resources.resource_filename(__name__, r'./examples/0615610.order.json')).read())
    pallet_sim.show_3D_pallet(0)
    pallet_sim.show_3D_pallet(1)

def demo():
    from .pallet_sim import Pallet_Sim
    pallet_sim = Pallet_Sim()
    pallet_sim.load(json_data=open(pkg_resources.resource_filename(__name__, r'./examples/0615610.order.json')).read())
    pallet_sim.show_3D_pallet(0)


if __name__ == '__main__':
    main()
