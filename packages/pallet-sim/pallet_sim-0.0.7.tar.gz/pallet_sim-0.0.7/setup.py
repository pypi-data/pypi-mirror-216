from setuptools import setup, find_packages

setup(
    name='pallet_sim',
    version='0.0.7',
    author='Rodolfo Verde',
    description='Pallet simulation library developed at THWS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'pallet_sim': ['textures/*.stl'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        # Specify any dependencies required by your library
        # For example:
        # 'numpy>=1.11.1',
        'pyvista',
        'mujoco',
        'pybullet',
        'numpy-stl',
        'mujoco-python-viewer',
        'PyYAML'
    ],
)