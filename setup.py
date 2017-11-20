import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="restible",
    version=read('VERSION').strip(),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="MIT",
    keywords="restible REST restapi rest server restless",
    url="http://github.com/novopl/restible",
    description="Python library to help building RESTfull APIs",
    long_description=read('README.rst'),
    package_dir={'restible': 'src/restible'},
    packages=find_packages('src', exclude=('test', 'test.*')),
    install_requires=[
        l.strip() for l in read('ops/requirements.txt').split() if '==' in l
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
