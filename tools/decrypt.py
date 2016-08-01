import sys
import socket
import struct
import urllib2
import time
import hashlib

def decrypt(buffer):  
	for i in range(len(buffer)): 
		buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1
def encrypt(buffer):
	    for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

L1=''

L2 = []
packet = []
packet.append([int(i,16) for i in L1.split(':')])
print packet,str('\n')
decrypt(L2)
print L2,str('\n')
print L2[18:34],str('\n')
for i in L2:
	print i,hex(i),chr(i)
	