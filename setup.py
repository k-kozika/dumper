from setuptools import setup, find_packages


setup(
    name="dumper",
    version="0.0.1",
    author="Diazole",
    description="Dump L3 CDM from any Android device",
    packages=find_packages(),
    install_requires=[
        "frida",
        "protobuf",
        "pycryptodome"
    ],
)
