#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="NDOP",
    version="0.2.0",
    packages=find_packages(),
    # scripts = ['ndop/ndop.py'],

    install_requires=[
        "psutil >= 0.7.1",
        "pylibpcap >= 0.6.4",
        "tornado >= 0.0.0"
    ],

    author='Olivier BLIN',
    author_email='olivier.oblin@gmail.com',
    description="Network sniffer with websockets",
    long_description=open('README.txt').read(),
    keywords="sniffer websocket network",
    url='https://github.com/OlivierB/Network-Display-On-Pi.git',
    license='',
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
