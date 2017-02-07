#!/usr/bin/python
#-*-coding:utf-8-*-
import ConfigParser
import os

def confread():
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    username = conf.get("conf", "username")
    password = conf.get("conf", "password")
    host = conf.get("conf", "host")
    ver = conf.get("conf", "version")
    ser = conf.get("conf", "services")
    savepass = conf.get("conf", "savepassword")
    a = []
    a.append(username)
    a.append(password)
    a.append(host)
    a.append(ver)
    a.append(ser)
    a.append(savepass)
    return a


def confcr():
    f = file("conf.ini", "w+")
    con = ["[conf]\n", "username = \n", "password = \n", "host = 210.45.194.10\n",
           "version = 3.6.4\n", "services = int\n", "savepassword = 0"]
    f.writelines(con)
    f.close()


def confwriteu(a):
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "username", a)
    conf.write(open("conf.ini", "w"))


def confwritep(a):
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "password", a)
    conf.write(open("conf.ini", "w"))


def confwriteh(a):
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "host", a)
    conf.write(open("conf.ini", "w"))


def confwritev(a):

    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "version", a)
    conf.write(open("conf.ini", "w"))


def confwrites(a):
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "services", a)
    conf.write(open("conf.ini", "w"))


def confwritesp(a):
    conf = ConfigParser.ConfigParser()
    conf.read("conf.ini")
    conf.set("conf", "savepassword", a)
    conf.write(open("conf.ini", "w"))


def init():
    filename = r'conf.ini'
    if os.path.exists(filename):
        f = open(filename, "r")
        content = f.read()
        f.close()
        if "username" in content and "password" in content and "host" in content and "version" in content and "services" in content and "savepassword" in content:
                return True
        else:
                confcr()
                return True
    else:
        confcr()
        return True
    
