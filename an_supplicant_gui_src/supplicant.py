#!/usr/bin/python
'''
Start function.
if conf.ini is exist
then start supplicant_dev project
else conf.ini is no exist
creat it.
'''
import supplicantdev
from func import config_r_w


if config_r_w.init():
    supplicantdev.main()
