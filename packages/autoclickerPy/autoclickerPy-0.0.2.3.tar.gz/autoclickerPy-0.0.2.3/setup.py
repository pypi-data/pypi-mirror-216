from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2.3'
DESCRIPTION = 'Simple autoclicker for python'
LONGDESCRIPTION = 'Simple autoclicker for python long description'

# Setting up
setup(
    name="autoclickerPy",
    version=VERSION,
    author="Geo",
    author_email="<geocraft31@gamil.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pynput', 'six'],
    keywords=['python', 'autoclicker'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)