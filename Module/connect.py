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

def send(sock,packet):
	host = gethost()
	port = 3848
	sock.sendto(packet, (host, port))

def upnet(sock, packet):
	send(sock,packet)
	upnet_ret = sock.recv(3848)
	upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
	decrypt(upnet_ret)
	status2 = upnet_ret[20]
	session_len = upnet_ret[22]
	session = upnet_ret[23:session_len + 23]
	message_len = upnet_ret[upnet_ret.index(11,35)+1]
	message = upnet_ret[upnet_ret.index(11,35)+2:message_len+upnet_ret.index(11,35)+2]
	message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
	print message
	if status2==0:
		sock.close()
		sys.exit()
	else:
			return session
	
def breathe(sock, mac_address, ip, session, index):
	time.sleep(0) 
	while True:
		breathe_packet = generate_breathe(mac_address, ip, session, index)
		send(sock,breathe_packet)
		try:
			breathe_ret = sock.recv(3848)
		except socket.timeout:
			continue
		else:
			status = struct.unpack('B' * len(breathe_ret), breathe_ret)
			if status[20] == 0:
				sock.close()
				sys.exit()
			index += 3
			try:
				time.sleep(30)
			except KeyboardInterrupt:
				downnet_packet = generate_downnet(mac_address,ip,session,index)
				send(sock,downnet_packet)
				print str('\n'),str('You have been downnet.')
				sock.close()
				sys.exit()