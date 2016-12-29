#!/usr/bin/python
import supplicantdev
import confrw
import os

 
def get_text_file(filename):
        f = open(filename, "r")
        content = f.read()
        f.close() 
        return content


filename = r'conf.ini'
if os.path.exists(filename):
    b=get_text_file(filename)
    if "username" in b and "password" in b and "host" in b and "version" in b and "services" in b and "savepassword" in b:
        supplicantdev.main()
    #os.remove(filename)
    else:
        confrw.confcr()
        supplicantdev.main()
else:
    confrw.confcr()
    supplicantdev.main()

