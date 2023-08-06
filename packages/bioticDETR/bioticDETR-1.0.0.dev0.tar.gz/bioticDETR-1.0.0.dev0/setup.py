
"""bioticDETR build script for setuptools.

"""


import setuptools


with open("README.rst", "r") as readme_file:
    readme_description = readme_file.read()

setuptools.setup(
    name="bioticDETR",
    version="1.0.0.dev0",
    author="Calvin",
    author_email="calvin.isotope@gmail.com",
    description="Detection Transformers for Biotic Interactions",
    long_description=readme_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/IsotopeC/bioticDETR",
    packages=setuptools.find_packages(exclude=['docs', 'tests', 'logs', 'examples']),
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    keywords='DETR AI Biotic Interactions',
    install_requires=['numpy', 'pandas'],
    python_requires='>3.9'
)
