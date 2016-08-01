import sys
import socket
import struct
import urllib2
import time
import hashlib

def encrypt(buffer):
	    for i in range(len(buffer)):
		buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7
def decrypt(buffer):  #
	for i in range(len(buffer)): #
		buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1        
	
L=[]
mac = ''
user = ''
pwd = ''
ip=''
packet = []
packet.append(1)
packet_len = len(user) + len(pwd) + 60
packet.append(packet_len)
packet.extend([i * 0 for i in range(16)])
packet.extend([7, 8])
packet.extend([int(i, 16) for i in mac.split('-')])
packet.extend([1, len(user) + 2])
packet.extend([ord(i) for i in user])
packet.extend([2, len(pwd) + 2])
packet.extend([ord(i) for i in pwd])
packet.extend([9, len(ip) + 2])
packet.extend([ord(i) for i in ip])
packet.extend([10, 5, 105, 110, 116, 14, 3, 1, 31, 7, 51, 46, 55, 46, 52])
md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()   
packet[2:18] = struct.unpack('16B', md5)    #      
print str('1:'),packet[0:1]
print '\n'
print str('2 is len packet:'),packet[1:2]
print '\n'
print str('3 to 18 is md5:'),packet[2:18]
print '\n'
print str('19 to 20 is still 7,8:'),packet[18:20]
print '\n'
print str('21 to 26 is ord macaddress:'),packet[20:26]
hexi= [hex(i) for i in packet[20:26]]
print str('Mac address in 21 to 26:'),hexi
print '\n'
print str('UserLen'),len(user)
print '\n'
print str('27 to 28 is 1,userlen+2:'),packet[26:28]
print '\n'
print str('29 to 29+userlen-1 is user:'),packet[28:28+len(user)]
print '\n'
print str('pwdlen is :'),len(pwd)
print '\n'
print str('29+userlen to 30+userlen is 2,pwdlen+2:'),packet[28+len(user):28+2+len(user)]
print '\n'
print str('31+userlen to 31+userlen+pwdlen-1 is pwd:'),packet[28+2+len(user):28+2+len(user)+len(pwd)]
print '\n'
print str('lenip is :'),len(ip)
print '\n'
print str('31+pwdlen+userlen to 32+pwdlen+userlen is 9,iplen+2:'),packet[30+len(user)+len(pwd):32+len(user)+len(pwd)]
print '\n'
print str('33+pwdlen+userlen to 32+pwdlen+userlen+iplen is ip'),packet[32+len(user)+len(pwd):32+len(user)+len(pwd)+len(ip)]
print '\n'
print str('33+pwdlen+userlen+iplen to end '),packet[32+len(user)+len(ip)+len(pwd):]
print '\n'
print str('packetlenth:'),len(packet)
print '\n'
print str('all len is :'),len(user)+len(pwd)+len(ip)+14+33
print '\n'
stri=[i for i in packet]
print str('all uncrypt:\n'),stri
print '\n'
stri=[chr(i) for i in packet]
new=zip(packet,stri)
print str('uncrypt and ascii is :'),new[26:]
encrypt(packet)
stri=[hex(i) for i in packet]
print '\n'
print str('hex and crypt:\n'),stri


