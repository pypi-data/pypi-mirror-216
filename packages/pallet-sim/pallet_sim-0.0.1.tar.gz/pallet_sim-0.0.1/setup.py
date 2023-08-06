from setuptools import setup, find_packages

setup(
    name='pallet_sim',
    version='0.0.1',
    author='Rodolfo Verde',
    description='Pallet simulation library developed at THWS',
    packages=find_packages(),
    package_data={
        'pallet_sim': ['textures/*.stl'],
    },
)
