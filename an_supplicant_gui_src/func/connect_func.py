#!/usr/bin/python
#-*-coding:utf-8-*-
'''
This function is use for:
Login in,
keep online,
Login out. 
'''
import en_de_crypt_func
import socket
import struct


def upnet(sock, packet, host, getsession):
    sock.settimeout(3)
    try:
        sock.sendto(packet, (host, 3848))
        upnet_ret = sock.recv(3848)
        upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
        en_de_crypt_func.decrypt(upnet_ret)
        status2 = upnet_ret[20]
        session_len = upnet_ret[22]
        session = upnet_ret[23:session_len + 23]
        message_len = upnet_ret[upnet_ret.index(11, 35) + 1]
        message = upnet_ret[upnet_ret.index(
            11, 35) + 2:message_len + upnet_ret.index(11, 35) + 2]
        message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
        if status2 == 0:
            getsession = []
            return status2, message
        else:
            for i in session:
                getsession.append(i)
            return status2, message
    except socket.timeout:
        getsession = []
        status2 = 0
        message = u'服务器无回应'
        return status2, message


def breathe(sock, packet, host):
    sock.settimeout(5)
    try:
        sock.sendto(packet, (host, 3848))
        upnet_ret = sock.recv(3848)
        upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
        en_de_crypt_func.decrypt(upnet_ret)
        status2 = upnet_ret[20]
        return status2
    except socket.timeout:
        status2 = 0
        return status2


def downnet(sock, packet, host):
    sock.sendto(packet, (host, 3848))
    sock.close()
