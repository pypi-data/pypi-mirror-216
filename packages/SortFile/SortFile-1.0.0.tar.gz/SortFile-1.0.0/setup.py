import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'A package for sorting files based on a specified pattern.'

# Setting up
setup(
    name="SortFile",
    version=VERSION,
    author="Wissam Al-Kahwaji",
    author_email="wissamalkahwaji@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'SortFile = SortFile.main:main',
        ],
    },
    keywords=['python', 'Sort', 'SortFile', 'Sorting', 'Data'],
)
