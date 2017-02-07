#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
an_supplicant_GUI setup file.
ONLY FOR MAC OS!
Usage:
    cd /an_supplicant_gui_src 
    py2applet --make-setup supplicant.py
    python setup.py py2app
"""

from setuptools import setup

APP = ['supplicant.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
