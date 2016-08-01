#!/usr/bin/python
# -*- coding utf-8 -*-

import struct
def encrypt(buffer):
	for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

def decrypt(buffer):
	for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1
pac=''
L2=[]
packet=[]
packet.append([int(i,16) for i in pac.split(':')])
print packet,str('\n')
decrypt(L2)
print L2
session_len = L2[22]
print str('sesssion len is'),session_len
session = L2[23:session_len + 23]
p=L2.index(11)
message_len = L2[L2.index(11)+1]
print message_len
message = L2[L2.index(11)+2:message_len + L2.index(11)+2]
print message
message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
print message
print message_len
for i in L2:
	print i,chr(i)