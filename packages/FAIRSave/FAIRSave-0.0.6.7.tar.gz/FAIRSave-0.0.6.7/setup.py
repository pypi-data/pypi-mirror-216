from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="FAIRSave",
    version="0.0.6.7",
    project_urls={"GitLab": "https://gitlab.com/linked-tribological-data/fair-save/FAIR-Save_Utilities",
                  "Changelog": "https://gitlab.com/linked-tribological-data/fair-save/FAIR-Save-Utilities/-/blob/main/Changelog.md"},
    author="Malte Flachmann, Floriane Bresser, Ilia Bagov (Karlsruhe Institute of Technology)",
    author_email="malte.flachmann@student.kit.edu",
    license="Apache-2.0",
    description="Package to run the FAIR-Save toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords="Kadi4Mat, FAIR",
    python_requires='>=3.10',
    install_requires=['kadi-apy==0.25.0',
                      'xmltodict>=0.13.0',
                      'nested_lookup>=0.2.25']
    )
