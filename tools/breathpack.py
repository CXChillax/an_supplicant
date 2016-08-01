#!/usr/bin/python
import hashlib
import struct
def encrypt(buffer):
	for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

def decrypt(buffer):
	for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1 

mac = ''
ip = ''
username = ''
password = ''
index = 0x01000000
index = hex(index)[2:]
packet = []
session=[]
packet.append(3)
packet_len = len(session) + 88
packet.append(packet_len)
packet.extend([i * 0 for i in range(16)])
packet.extend([8, len(session) + 2])
packet.extend(session)
packet.extend([9, 18])
packet.extend([ord(i) for i in ip])
packet.extend([i * 0 for i in range(16 - len(ip))])
packet.extend([7, 8])
packet.extend([int(i, 16) for i in mac.split(':')])
packet.extend([20, 6])
print packet
packet.extend([int(index[0:-6],16), int(index[-6:-4],16), int(index[-4:-2],16), int(index[-2:],16)])
packet.extend([42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0, 0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0, 0, 0])
md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
packet[2:18] = struct.unpack('16B', md5)
print str('md5 is:'),packet[2:18],str('\n')
print packet
print str('\n')
encrypt(packet)
print packet,str('\n')
ct=[hex(i) for i in packet]
print ct

		
		