import os
import pkg_resources


# function used to load example data contain in example_data folder
def load_example_data():
    data = []
    for file in os.listdir(pkg_resources.resource_filename(__name__, r'./example_data')):
        if file.endswith(".order.json"):
            data.append(open(pkg_resources.resource_filename(__name__, r'./example_data/' + file)).read())
    return data
