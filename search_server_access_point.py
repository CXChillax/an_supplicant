# !/usr/bin/python
# -*-coding:utf-8-*-
# bugreport:lyq19961011@gmail.com
import socket
import struct
import hashlib


def send_data(host, sock, packet, port):
    sock.sendto(packet, (host, port))
    
def check_md5(md5,md5_recv):
    for i in range(16):
        if md5[i] != md5_recv[i]:
            print md5[i],md5_recv[i]
    return True

def encrypt(packet):
    return_packet=[]
    for i in packet:
        i = (i & 0x80) >> 6 | (i & 0x40) >> 4 | (i & 0x20) >> 2 | (i & 0x10) << 2 | (
            i & 0x08) << 2 | (i & 0x04) << 2 | (i & 0x02) >> 1 | (i & 0x01) << 7
        return_packet.append(i)
    return return_packet

def decrypt(packet):
    return_packet=[]
    for i in packet:
        i = (i & 0x80) >> 7 | (i & 0x40) >> 2 | (i & 0x20) >> 2 | (i & 0x10) >> 2 | (
            i & 0x08) << 2 | (i & 0x04) << 4 | (i & 0x02) << 6 | (i & 0x01) << 1
        return_packet.append(i)
    return return_packet

def search_service(ip,mac,host_ip):
    packet = []
    packet.append(0x07)
    packet_len = 1+1+16+1+1+5+1+1+6
    packet.append(packet_len)
    packet.extend([i*0 for i in range(16)])
    packet.append(0x08)
    packet.append(0x07)
    packet.extend([i*1 for i in range(5)])
    packet.append(0x07)
    packet.append(0x08)
    packet.extend([int(i,16) for i in mac.split(':')])
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    packet = encrypt(packet)
    packet = b''.join([struct.pack('B', i) for i in packet])
    send_data(host_ip, sock_udp, packet, 3848)
    packet_recv = sock_udp.recv(4096)
    packet_recv = [i for i in struct.unpack('B' * len(packet_recv), packet_recv)]
    packet_recv = decrypt(packet_recv)
    md5_recv = packet_recv[2:18]
    packet_recv[2:18] = [i*0 for i in range(16)]
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet_recv])).digest()

    md5 = struct.unpack('16B',md5)
    if check_md5(md5,md5_recv) is True:
        service_index =  packet_recv.index(10)
        service_len = packet_recv[service_index+1]-2
        service = packet_recv[service_index+2:service_index+2+service_len]
        print 'search service success:'
        stra = ''
        for i in service:
            stra += chr(i)
        print stra
    else:
        print 'md5 error!'
    
def search_server_ip(ip,mac):
    packet = []
    packet.append(0x0c)
    packet_len = 1+1+16+1+1+5+1+1+16+1+1+6
    packet.append(packet_len)
    packet.extend([i*0 for i in range(16)])
    packet.append(0x08)
    packet.append(0x07)
    packet.extend([i*1 for i in range(5)])
    packet.append(0x09)
    packet.append(0x12)
    packet.extend([ord(i) for i in ip])
    packet.extend([i*0 for i in range(16-len(ip))])
    packet.append(0x07)
    packet.append(0x08)
    packet.extend([int(i,16) for i in mac.split(':')])
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    packet = encrypt(packet)
    packet = b''.join([struct.pack('B', i) for i in packet])
    send_data('1.1.1.8', sock_udp, packet, 3850)
    packet_recv = sock_udp.recv(4096)
    packet_recv = [i for i in struct.unpack('B' * len(packet_recv), packet_recv)]
    packet_recv = decrypt(packet_recv)
    md5_recv = packet_recv[2:18]
    packet_recv[2:18] = [i*0 for i in range(16)]
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet_recv])).digest()

    md5 = struct.unpack('16B',md5)
    if check_md5(md5,md5_recv) is True:
        #print packet_recv
        server_index =  packet_recv.index(0x0c)
        server = packet_recv[server_index+2:server_index+6]
        print 'search host ip success:'
        stra = ''
        for i in server:
            stra += str(i)+'.'
        print stra[:-1]
        return stra[:-1]
    else:
        print 'md5 error!'
    
if __name__ == '__main__':
    print 'This file is only use for search server ip and access point!'
    ip_addr = '192.168.1.1' #your IP address
    mac_addr = 'aa:aa:aa:aa:aa:aa'
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_udp.bind((ip_addr, 3848))
    except socket.error:
        print ('Bind port failed.Use random port')
        pass
    host_ip = search_server_ip(ip_addr, mac_addr)
    search_service(ip_addr,mac_addr,host_ip)
