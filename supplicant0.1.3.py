#!/usr/bin/python
#-*-coding:utf-8-*-
# 如果遇到中文不能显示中文，请删除所有中文，并设置不显示服务器消息
# bugreport:lyq19961011@gmail.com
import sys
import socket
import struct
import time
import hashlib



def define_host():
    host='210.45.194.10'   #填上学校服务器IP,例如'210.45.194.10'
    return host

def send_data(sock,packet):
    host = define_host()
    port = 3848   #端口
    sock.sendto(packet, (host, port))

def login(sock, packet, message_display):
    send_data(sock,packet)
    response = sock.recv(3848)
    response = [i for i in struct.unpack('B' * len(response), response)]
    decrypt(response)
    login_status = response[20]
    session_len = response[22]
    session = response[23:session_len + 23]
    message_len = response[response.index(11,35)+1]
    message = response[response.index(11,35)+2:message_len+response.index(11,35)+2]
    message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
    if login_status == 0:
        if message_display == '1':
            print message
            sock.close()
            sys.exit()
        else:
            print str('Login fail')
            sock.close()
            sys.exit()

    elif message_display == '1':
        print message
        return session
    else:
        print str('Login success')
        return session
    
def breathe(sock, mac_address, ip, session, index, block):
    time.sleep(0) 
    while True:
        breathe_packet = generate_breathe(mac_address, ip, session, index, block)
        send_data(sock,breathe_packet)
        try:
            breathe_response = sock.recv(3848)
        except socket.timeout:
            continue
        else:
            breathe_status = struct.unpack('B' * len(breathe_response), breathe_response)
            if breathe_status[20] == 0:
                sock.close()
                sys.exit()
            index += 3
            try:
                time.sleep(30)
            except KeyboardInterrupt:
                downnet_packet = generate_downnet(mac_address,ip,session,index,block)
                send_data(sock,downnet_packet)
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
    packet.append(0x01)
    packet_len = 38 + len(user)  + len(pwd)  + len(ip)  + len(service)  + len(dhcp) + len(version)
    packet.append(packet_len)
    packet.extend([i * 0x00 for i in range(16)])
    packet.extend([0x07,0x08])
    packet.extend([int(i,16) for i in mac.split(':')])
    packet.extend([0x01, len(user) + 2])
    packet.extend([ord(i) for i in user])
    packet.extend([0x02, len(pwd) + 2])
    packet.extend([ord(i) for i in pwd])
    packet.extend([0x09, len(ip) + 2])
    packet.extend([ord(i) for i in ip])
    packet.extend([0x0a, len(service)+2])
    packet.extend([ord(i) for i in service])
    packet.extend([0x0e, len(dhcp)+2]) 
    packet.extend([ord(i) for i in dhcp])
    packet.extend([0x1f, len(version)+2])
    packet.extend([ord(i) for i in version])
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet
    
def generate_breathe(mac, ip, session, index, block):
    index = hex(index)[2:]
    packet = []
    packet.append(0x03)
    packet_len = len(session) + 88
    packet.append(packet_len)
    packet.extend([i * 0 for i in range(16)])
    packet.extend([0x08, len(session) + 2])
    packet.extend(session)
    packet.extend([0x09, 0x12])
    packet.extend([ord(i) for i in ip])
    packet.extend([i * 0 for i in range(16 - len(ip))])
    packet.extend([0x07, 0x08])
    packet.extend([int(i, 16) for i in mac.split(':')])
    packet.extend([0x14, 0x06])
    packet.extend([int(index[0:-6],16), int(index[-6:-4],16), int(index[-4:-2],16), int(index[-2:],16)])
    packet.extend(i for i in block)
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet

def generate_downnet(mac, ip, session, index, block):
    index = hex(index)[2:]
    packet = []
    packet.append(0x05)
    packet_len = len(session) + 88
    packet.append(packet_len)
    packet.extend([i * 0 for i in range(16)])
    packet.extend([0x08, len(session) + 2])
    packet.extend(session)
    packet.extend([0x09, 0x12])
    packet.extend([ord(i) for i in ip])
    packet.extend([i * 0 for i in range(16 - len(ip))])
    packet.extend([0x07, 0x08])
    packet.extend([int(i, 16) for i in mac.split(':')])
    packet.extend([0x14, 0x06])
    packet.extend([int(index[0:-6],16), int(index[-6:-4],16), int(index[-4:-2],16), int(index[-2:],16)])
    packet.extend(i for i in block)
    md5 = hashlib.md5(''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    encrypt(packet)
    packet = ''.join([struct.pack('B', i) for i in packet])
    return packet

def decode():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
def main():
    decode()
    host = define_host()
    mac_address = ''    #MAC地址,例如'AA:AA:AA:AA:AA'
    ip = ''           #IP地址,例如'192.168.1.1'
    username = ''    #用户名,例如'jack'
    password = ''    #密码,例如'123456'
    version = '3.6.4'  #安腾客户端版本号设置,例如'3.6.5'
    dhcp_setting = '0'   #是否开启DHCP自分配IP地址,'1'或'0' 
    service = 'int'     #服务设置,例如'int','internet'
    message_display = '1' #是否显示服务器返回的消息,'1'或'0' 
    
    print str('Ctrl + C to exit\nMAC:'),mac_address,str('\nHOST:'),host,str('\nIP:'),ip
    index = 0x01000000
    block = [0x2a, 0x06, 0, 0, 0, 0, 0x2b, 0x06, 0, 0, 0, 0, 0x2c, 0x06, 0, 0, 0, 0, 0x2d, 0x06, 0, 0, 0, 0, 0x2e, 0x06, 0, 0, 0, 0, 0x2f, 0x06, 0, 0, 0, 0]
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    upnet_packet = generate_upnet(mac_address, username, password,  ip, dhcp_setting, service, version)
    session = login(sock, upnet_packet ,message_display)
    breathe(sock, mac_address, ip, session, index, block)
    
if __name__ == '__main__':
    main()
