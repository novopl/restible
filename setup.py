import os
import re
from setuptools import setup, find_packages


RE_PY_VERSION = re.compile(
    r'__version__\s*=\s*["\']'
    r'(?P<version>\d+(\.\d+(\.\d+)?)?)'
    r'["\']'
)

def read_version():
    content = read('src/restible/__init__.py')
    m = RE_PY_VERSION.search(content)
    if not m:
        return '0.0'
    else:
        return m.group('version')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="restible",
    version=read_version(),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="MIT",
    keywords="restible REST restapi rest server restless",
    url="http://github.com/novopl/restible",
    description="Python library to help building RESTful APIs",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('test', 'test.*')),
    install_requires=[
        l.strip() for l in read('requirements.txt').split()
        if l.strip() and not l.lstrip().startswith('#')
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
