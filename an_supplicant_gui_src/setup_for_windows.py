#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
An_Supplicant_GUI setup file.
ONLY FOR WINDOWS!
Usage:
    cd an_supplicant_gui_src
    python setup.py py2exe
"""

from distutils.core import setup
import py2exe


setup(windows=['supplicant.py'])
