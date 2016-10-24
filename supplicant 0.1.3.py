#!/usr/bin/python
#-*-coding:utf-8-*-
# 如果遇到中文不能显示请删除所有中文，并设置不显示服务器消息
# bugreport:lyq19961011@gmail.com
import sys
import socket
import struct
import time
import hashlib



def gethost():
    host='210.45.194.10'   #填上学校服务器IP,例如'210.45.194.10'
    return host



def send(sock,packet):
    host = gethost()
    port = 3848   #端口
    sock.sendto(packet, (host, port))

def upnet(sock, packet, message_display):
    send(sock,packet)
    upnet_ret = sock.recv(3848)
    upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
    decrypt(upnet_ret)
    status2 = upnet_ret[20]
    session_len = upnet_ret[22]
    session = upnet_ret[23:session_len + 23]
    message_pos = 23 + session_len
    message_len = upnet_ret[message_pos + 1]
    message = upnet_ret[message_pos+2:message_len+message_pos+2]
    message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
    if status2==0:
        if message_display=='1':
            print message
            sock.close()
            sys.exit()
        else:
            print str('Login fail')
            sock.close()
            sys.exit()

    elif message_display=='1':
        print message
        return session
    else:
        print str('Login success')
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
                print str('\n'),str('Downnet success.')
                sock.close()
                sys.exit()

                
    
def encrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7

def decrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1        
        
def generate_upnet(mac, user, pwd,  ip, dhcp, service, version):
    packet = []
    packet.append(1)
    packet_len = 1 + 1 + 16 + 2 + 6 + 2 + len(user) + 2 + len(pwd) + 2 + len(ip) + 2 + len(service) + 2 + len(dhcp) + 2 + len(version)
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
    packet.extend([10, len(service)+2])
    packet.extend([ord(i) for i in service])
    packet.extend([14, len(dhcp)+2]) 
    packet.extend([ord(i) for i in dhcp])
    packet.extend([31, len(version)+2])
    packet.extend([ord(i) for i in version])
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

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    mac_address = ''    #MAC地址,例如'AA:AA:AA:AA:AA'
    ip = ''           #IP地址,例如'192.168.1.1'
    host = gethost()  
    print str('Ctrl + C to exit\nMAC:'),mac_address,str('\nHOST:'),host,str('\nIP:'),ip
    username = ''    #用户名,例如'jack'
    password = ''    #密码,例如'123456'
    version = '3.6.5'  #安腾客户端版本号设置,例如'3.6.5'
    dhcp_setting = '0'   #是否开启DHCP自分配IP地址,'1'或'0' 
    service = 'int'     #服务设置,例如'int','internet'
    message_display = '1' #是否显示服务器返回的消息,'1'或'0' 
    index = 0x01000000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    upnet_packet = generate_upnet(mac_address, username, password,  ip, dhcp_setting, service, version)
    session = upnet(sock, upnet_packet ,message_display)
    breathe(sock, mac_address, ip, session, index)
    
if __name__ == '__main__':
    main()
