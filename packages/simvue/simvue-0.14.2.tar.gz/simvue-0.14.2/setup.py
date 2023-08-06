import re
import setuptools

with open('simvue/version.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simvue",
    version=version,
    author_email="info@simvue.io",
    description="Simulation tracking and monitoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://simvue.io",
    platforms=["any"],
    install_requires=["dill", "requests", "msgpack", "tenacity", "pandas", "pyjwt", "psutil", "pydantic==1.10.7", "plotly"],
    package_dir={'': '.'},
    packages=["simvue"],
    package_data={"": ["README.md"]},
    scripts=["bin/simvue_sender"]
)
