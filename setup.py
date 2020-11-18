from setuptools import setup 

with open("requirements.txt") as r : 
    requirements = r.read().splitlines()

setup(
        name="pymongobox",
        version="0.0.1",
        author="Pierre Kieffer",
        packages=["pymongobox.crud", "pymongobox.streaming"],
        install_requires=requirements
        )

