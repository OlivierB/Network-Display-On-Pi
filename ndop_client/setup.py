#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="NDOP-Client",
    version="0.0.2",
    packages=find_packages(),

    install_requires=[
        # "curses >= 0.0.0",
        "websocket >= 0.2.1",
        "argparse >= 1.2.1"
    ],

    author='Olivier BLIN',
    author_email='olivier.oblin@gmail.com',
    description="NDOP light and simple client",
    keywords="sniffer websocket network",
    url='https://github.com/OlivierB/Network-Display-On-Pi.git',
    license='',
    entry_points={"console_scripts": ["ndop-client=ndop_client.client:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
    ],
)

