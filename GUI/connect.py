#!/usr/bin/python

import encrypt
import socket
import struct


def upnet(sock, packet, host, getsession):
	sock.sendto(packet,(host,3848))
	upnet_ret = sock.recv(3848)
	upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
	encrypt.decrypt(upnet_ret)
	status2 = upnet_ret[20]
	session_len = upnet_ret[22]
	session = upnet_ret[23:session_len + 23]
	message_len = upnet_ret[upnet_ret.index(11,35)+1]
	message = upnet_ret[upnet_ret.index(11,35)+2:message_len+upnet_ret.index(11,35)+2]
	message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
	for i in session:
		getsession.append(i)
	return status2,message

	
def breathe(sock, packet, host):
	sock.sendto(packet,(host,3848))
	upnet_ret = sock.recv(3848)
	upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
	encrypt.decrypt(upnet_ret)
	status2 = upnet_ret[20]
	return status2

def downnet(sock, packet, host):
	sock.sendto(packet,(host,3848))
	sock.close()