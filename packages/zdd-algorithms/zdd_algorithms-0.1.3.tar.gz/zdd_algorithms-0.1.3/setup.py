from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.3'
DESCRIPTION = 'A package that implements zdd algorithms'
LONG_DESCRIPTION = 'This package implements all the algorithms described on the wiki page of zdds+\
        (union, intersection, difference, subset0, subset1, change and count). +\
        They are not optimized and without caching. This package should be used to learn zdds and +\
        play around with them. In addition to the algorithms there is also a visualization function and functions +\
        that can make a zdd out of a set and vice versa.'


# Setting up
setup(
    name="zdd_algorithms",
    version=VERSION,
    author="Thilo Langensteiner",
    author_email="<thilo.j.la@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    project_urls = {"GitHub":"https://github.com/Thilo-J/zdd_algorithms"},
    url="https://github.com/Thilo-J/zdd_algorithms",
    
    packages=find_packages(),
    install_requires=['graphviz'],
    keywords=['python', 'zdd', 'bdd', 'zsdd', 'zero-suppressed', 'decision diagram'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)