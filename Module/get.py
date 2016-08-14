#!/usr/bin/python
import sys
import socket
import struct
import urllib2
import time
import hashlib
import uuid
import get
import encrypt
import packet
import connect
import sys
import socket
import struct

def get_mac_address(): 
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
	return ":".join([mac[e:e+2] for e in range(0,11,2)])

def gethost():
	host='210.45.194.10'
	return host

def Get_local_ip():
	try:
		csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		csock.connect(('8.8.8.8', 80))
		(addr, port) = csock.getsockname()
		csock.close()
		return addr
	except socket.error:
		return "127.0.0.1"