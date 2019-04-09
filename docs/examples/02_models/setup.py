# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="restiblog",
    version='0.1.0',
    author="Mateusz 'novo' Klos",
    license="MIT",
    url="http://github.com/novopl/restible/tree/docs/examples/02_models",
    description="Example app for restible tutorial",
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('test', 'test.*')),
    install_requires=[
        'Flask==1.0.2',
        'Flask-SQLAlchemy==2.3.2',
        'restible==0.11.11',
        'restible-flask==0.2.2',
        'serafin==0.12.2',
        'serafin-sqlalchemy==0.2',
    ],
    entry_points={
        'console_scripts': [
            'restiblog = restiblog.app:run_devserver',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
