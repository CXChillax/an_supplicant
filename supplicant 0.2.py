#!/usr/bin/python
# -*- coding utf-8 -*-
# bugreport:lyq19961011@gmail.com
import sys
import socket
import struct
import urllib2
import time
import hashlib
import getpass
import uuid

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
        main()
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

def encrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

def decrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1        
        
def generate_upnet(mac, ip, user, pwd):
    packet = []
    packet.append(1)
    packet_len = len(user) + len(pwd) + 60
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
    packet.extend([10, 5, 105, 110, 116, 14, 3, 1, 31, 7, 51, 46, 54, 46, 53])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet
    
def generate_breathe(mac, ip, session, index):
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
    packet.extend([int(index[0:-6],16), int(index[-6:-4],16), int(index[-4:-2],16), int(index[-2:],16)])
    packet.extend([42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0, 0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0, 0, 0])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet

def generate_downnet(mac, ip, session, index):
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
    packet.extend([int(index[0:-6],16), int(index[-6:-4],16), int(index[-4:-2],16), int(index[-2:],16)])
    packet.extend([42, 6, 0, 0, 0, 0, 43, 6, 0, 0, 0, 0, 44, 6, 0, 0, 0, 0, 45, 6, 0, 0, 0, 0, 46, 6, 0, 0, 0, 0, 47, 6, 0, 0, 0, 0])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet

def input_():
    username = raw_input("Username:")
    password = getpass.getpass("Password:")
    choose = username,password
    if '' in choose:
        print 'Username or password is empty!'
        input_()
    else:
        return username,password

def main():
    mac_address = get_mac_address()
    ip = Get_local_ip()
    host = gethost()
    print str('Notice: Ctrl + C to exit\nMAC:'),mac_address,str('\nHOST:'),host,str('\nIP:'),ip
    username,password = input_()
    index = 0x01000000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    upnet_packet = generate_upnet(mac_address, ip, username, password)    
    session = upnet(sock, upnet_packet)
    breathe(sock, mac_address, ip, session, index)

if __name__ == '__main__':
    main()
