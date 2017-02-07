#!/usr/bin/python
'''
This function is use for creat Bytes Stream.
'''
import hashlib
import en_de_crypt_func
import struct


def generate_upnet_packet(mac, ip, user, pwd, service, version):
    packet = []
    packet.append(1)
    packet_len = 39 + len(user) + len(pwd) + len(ip) + \
        len(service) + len(version)
    packet.append(packet_len)
    packet.extend([i * 0 for i in range(16)])
    packet.extend([7, 8])
    packet.extend([int(i, 16) for i in mac.split(':')])
    packet.extend([1, len(user) + 2])
    packet.extend([ord(i) for i in user])
    packet.extend([2, len(pwd) + 2])
    packet.extend([ord(i) for i in pwd])
    packet.extend([9, len(ip) + 2])
    packet.extend([ord(i) for i in ip])
    packet.extend([10, len(service) + 2])
    packet.extend([ord(i) for i in service])
    packet.extend([14, 3, 1])
    packet.extend([0x1f, len(version) + 2])
    packet.extend([ord(i) for i in version])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    en_de_crypt_func.encrypt(packet)
    packet_stream = ''.join([struct.pack('B', i) for i in packet])
    return packet_stream


def generate_breathe_packet(mac, ip, session, index):
    index = hex(index)[2:]
    packet = []
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
    packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16),
                   int(index[-4:-2], 16), int(index[-2:], 16)])
    packet.extend([42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0,
                   0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0, 0, 0])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    en_de_crypt_func.encrypt(packet)
    packet_stream = ''.join([struct.pack('B', i) for i in packet])
    return packet_stream


def generate_downnet_packet(mac, ip, session, index):
    index = hex(index)[2:]
    packet = []
    packet.append(5)
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
    packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16),
                   int(index[-4:-2], 16), int(index[-2:], 16)])
    packet.extend([42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0,
                   0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0, 0, 0])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    en_de_crypt_func.encrypt(packet)
    packet_stream = ''.join([struct.pack('B', i) for i in packet])
    return packet_stream
