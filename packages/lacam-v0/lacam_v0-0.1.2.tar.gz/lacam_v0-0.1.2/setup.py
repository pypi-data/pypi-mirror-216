from setuptools import setup, find_packages

setup(
    name="lacam_v0",
    version="0.1.2",
    author="Saullo",
    author_email="saullo.guilherme7@unifesspa.edu.br",
    description="A test library to LACAM - UNIFESSPA",
    packages=find_packages(where='src',),
    package_dir = {"": "src"},
    py_modules=["lacam_v0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
    )