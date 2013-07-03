#!/usr/bin/python
#encoding: utf-8

from distutils.core import setup

setup(
    name='NDOP',
    version='0.2.0',
    author='Olivier BLIN',
    author_email='olivier.oblin@gmail.com',
    packages=['ndop'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/OlivierB/Network-Display-On-Pi.git',
    license='',
    description="Network sniffer with websockets",
    long_description=open('README.txt').read(),
    keywords="sniffer websocket network",
    entry_points={"console_scripts": ["ndop=ndop.ndop:main"]},
    install_requires=[
        "psutil>=0.7.1",
        "python-libpcap>=0.6.4",
        "python-tornado",
    ],
)
