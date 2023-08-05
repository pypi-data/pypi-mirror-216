import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "platformer1234",
    version = "0.0.1",
    author = "Andy Z",
    author_email = "andyzhong147@gmail.com",
    description = ("An demonstration of how to upload project to pypi."),
    license = "MIT License",
    keywords = "tutorial",
    url = "",
    include_package_data = True,
    packages=['platformer1234'],
    package_data={'platformer1234':['*']},
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'pygame'
    ],
)