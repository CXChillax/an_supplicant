# !/usr/bin/python
# -*-coding:utf-8-*-
# bugreport:lyq19961011@gmail.com
import sys
import socket
import struct
import time
import hashlib


def send_data(host, sock, packet):
    sock.sendto(packet, (host, 3848))

def check_md5(md5,md5_recv):
    for i in range(16):
        if md5[i] != md5_recv[i]:
            return False
    return True

def login(host, sock, packet, message_display):
    send_data(host, sock, packet)
    while True:
        try:
            response = sock.recv(4096)
            response = [i for i in struct.unpack('B' * len(response), response)]
            response = decrypt(response)
            md5_recv = response[2:18]
            response[2:18] = [i*0 for i in range(16)]
            md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in response])).digest()
            md5 = struct.unpack('16B',md5)
            if check_md5(md5,md5_recv) is True:
                break
            response = []
        except socket.error:
            return False    
    login_status = response[20]
    session_len = response[22]
    session = response[23:session_len + 23]
    response[23:session_len+23]=[i*0 for i in range(session_len)]
    message_len = response[response.index(11) + 1]
    message = response[response.index(
        11) + 2:message_len + response.index(11) + 2]
    if login_status == 0:
        if message_display == '1':
            message = b''.join([struct.pack('B', i)
                               for i in message]).decode('gbk')
            print (message)
            return False
        else:
            return False
    elif message_display == '1':
        message = b''.join([struct.pack('B', i)
                           for i in message]).decode('gbk')
        print (message)
        return session
    else:
        print ('Login success')
        return session


def breathe(host, sock, mac_address, ip_addr, session, index, block):
    time.sleep(0)
    while True:
        breathe_packet = generate_breathe(
            mac_address, ip_addr, session, index, block)
        send_data(host, sock, breathe_packet)
        try:
            breathe_status = sock.recv(4096)
        except socket.timeout:
            return False
        breathe_status = [i for i in struct.unpack('B' * len(breathe_status), breathe_status)]
        breathe_status = decrypt(breathe_status)
        md5_recv = breathe_status[2:18]
        breathe_status[2:18] = [i*0 for i in range(16)]
        md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in breathe_status])).digest()
        md5 = struct.unpack('16B',md5)
        if check_md5(md5,md5_recv) is False:
            print 'md5 check failed!'
            return False
        if breathe_status[20] == 0:
            return False
        index += 3
        try:
            time.sleep(20)
        except KeyboardInterrupt:
            downnet_packet = generate_downnet(
                mac_address, ip_addr, session, index, block)
            send_data(host, sock, downnet_packet)
            print str('\n'), str('Downnet success.')
            sock.close()
            sys.exit()


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

def generate_upnet(mac, user, pwd, ip, dhcp, service, version):
    packet = []
    packet.append(0x01)
    packet_len = 38 + len(user) + len(pwd) + len(ip) + \
        len(service) + len(dhcp) + len(version)
    packet.append(packet_len)
    packet.extend([i * 0x00 for i in range(16)])
    packet.extend([0x07, 0x08])
    packet.extend([int(i, 16) for i in mac.split(':')])
    packet.extend([0x01, len(user) + 2])
    packet.extend([ord(i) for i in user])
    packet.extend([0x02, len(pwd) + 2])
    packet.extend([ord(i) for i in pwd])
    packet.extend([0x09, len(ip) + 2])
    packet.extend([ord(i) for i in ip])
    packet.extend([0x0a, len(service) + 2])
    packet.extend([ord(i) for i in service])
    packet.extend([0x0e, len(dhcp) + 2])
    packet.extend([ord(i) for i in dhcp])
    packet.extend([0x1f, len(version) + 2])
    packet.extend([ord(i) for i in version])
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    packet = encrypt(packet)
    packet = b''.join([struct.pack('B', i) for i in packet])
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
    packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16),
                   int(index[-4:-2], 16), int(index[-2:], 16)])
    packet.extend(i for i in block)
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    packet = encrypt(packet)
    packet = b''.join([struct.pack('B', i) for i in packet])
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
    packet.extend([int(index[0:-6], 16), int(index[-6:-4], 16),
                   int(index[-4:-2], 16), int(index[-2:], 16)])
    packet.extend(i for i in block)
    md5 = hashlib.md5(b''.join([struct.pack('B', i) for i in packet])).digest()
    packet[2:18] = struct.unpack('16B', md5)
    packet = encrypt(packet)
    packet = b''.join([struct.pack('B', i) for i in packet])
    return packet


def decode():
    reload(sys)
    sys.setdefaultencoding('utf-8')


def delay():
    time.sleep(10)


def main():
    if delay_enable == '1':
        delay()
    index = 0x01000000
    block = [0x2a, 0x06, 0, 0, 0, 0, 0x2b, 0x06, 0, 0, 0, 0, 0x2c, 0x06, 0, 0, 0,
             0, 0x2d, 0x06, 0, 0, 0, 0, 0x2e, 0x06, 0, 0, 0, 0, 0x2f, 0x06, 0, 0, 0, 0]
    while True:
        upnet_packet = generate_upnet(
            auth_mac_address, username, password, auth_ip, dhcp_setting, service_type, client_version)
        session = login(auth_host_ip, sock_udp,
                        upnet_packet, message_display_enable)
        if session is False:
            if reconnet_enable == '1':
                print ('Login failed..Relogining...')
                time.sleep(10)
                main()
            else:
                sock_udp.close()
                time.sleep(1)
                sys.exit()
        breathe_status = breathe(
            auth_host_ip, sock_udp, auth_mac_address, auth_ip, session, index, block)
        if breathe_status is False:
            if reconnet_enable == '1':
                print ('Breathe failed.Reconnecting...')
                time.sleep(10)
                main()
            else:
                print ('Breathe failed...')
                sock_udp.close()
                time.sleep(1)
                sys.exit()

if __name__ == '__main__':

    '''
    The auth_host_ip is the server ip such as '210.45.194.10'.
    The local_ip is the local host ip,use for bind send port.
        It can deffient from auth_ip,but must be correct.
    The auth_ip is the ip your wanna to auth.Such as your wireless router Ethernet IP.
    The service_type means the acess point services.Such as 'int','internet'.

    '''
    '''
    在auth_host_ip填上服务器的ip。
    在local_ip填上本机的IP地址，用于绑定发送报文的端口，所以一定要求是正确的。
    在auth_ip填上需要认证的IP地址，它可以是你的无线路由器的以太网地址。
    如果你没有用路由器，那么local_ip和auth_ip应是相同的。
    同样auth_mac_address需要填上你要认证的网卡的mac地址。例如路由器以太网卡，你的电脑的以太网卡。
    在service_type填上你需要认证的服务类型，我见过的有'int'，'internet'，如果你填的不对，服务器可能会返回"该账号服务不可用"。
    服务器和ip如果你不知道的话可以在另一个脚本search_server_access_point.py中搜寻到。
    '''
    auth_host_ip = '210.45.194.10'
    local_ip = '192.168.2.212'
    auth_ip = '172.17.142.146'
    auth_mac_address = 'aa:bb:cc:dd:ee:ff'
    username = 'jack'
    password = '123456'
    client_version = '3.6.4'
    service_type = 'int'
    dhcp_setting = '0'
    message_display_enable = '0'  # Display the  replay message from server.
    delay_enable = '0'  # Wait 10s to login in.  
    reconnet_enable = '1'  # Auto reconnect while your breathe fail or login fail.
    print ('Ctrl + C to Exit or Login out!')
    print ('Try to login in...')
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_udp.bind((local_ip, 3848))
    except socket.error:
        print ('Bind port failed.Use random port')
        pass
    sock_udp.settimeout(5)
    main()
