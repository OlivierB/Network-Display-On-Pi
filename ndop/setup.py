#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from ndop.config import server_conf

setup(
    name="NDOP",
    version=server_conf.__version__,
    packages=find_packages(),
    # scripts = ['ndop/ndop.py'],

    install_requires=[
        "psutil >= 0.7.1",
        "pylibpcap >= 0.6.4",
        "tornado >= 2.4.1",
        "argparse >= 1.2.1"
    ],

    author='Olivier BLIN',
    author_email='olivier.oblin@gmail.com',
    description="Network sniffer with websockets",
    long_description=open('README.txt').read(),
    keywords="sniffer websocket network",
    url='https://github.com/OlivierB/Network-Display-On-Pi.git',
    license='GPLv3',
    entry_points={"console_scripts": ["ndop=ndop.server:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
    ],
)
