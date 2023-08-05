import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "kennytestupload",
    version = "0.0.11",
    author = "Kenny C",
    author_email = "kennycheung388@yahoo.com.hk",
    description = ("An demonstration of how to upload project to pypi."),
    license = "MIT License",
    keywords = "tutorial",
    url = "",
    include_package_data = True,
    packages=['kennytestupload'],
    package_data={'kennytestupload':['*']},
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    # install_requires=[
    #     'pygame'
    # ],
)