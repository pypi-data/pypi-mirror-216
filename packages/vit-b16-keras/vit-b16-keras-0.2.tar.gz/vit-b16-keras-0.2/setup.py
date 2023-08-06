from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2'
DESCRIPTION = 'vit-b16-keras'
LONG_DESCRIPTION = 'A package to install vision transformer'

# Setting up
setup(
    name="vit-b16-keras",
    version=VERSION,
    author="Elena Paul",
    author_email="wohani7266@dotvilla.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tensorflow'],
    keywords=['arithmetic', 'math', 'mathematics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)