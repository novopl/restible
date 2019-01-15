# Copyright 2017-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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


# For dev environment or CI runs, install this package using `pip install .`
# For god knows why, if you install with python setup.py install or develop
# pylint will treat six as a local package and complain about import order o_O
setup(
    name="restible",
    version=read_version(),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="Apache 2.0",
    keywords="restible REST restapi rest server restless",
    url="http://github.com/novopl/restible",
    description="Python library to help building RESTful APIs",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('test', 'test.*')),
    install_requires=[
        'attrs>=17.0.0',
        'jsonschema~=2.6.0',
        'serafin>=0.11.0',
        'six>=1.0.0',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
