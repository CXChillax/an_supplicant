#!/usr/bin/python
import struct
a=[178, 187, 212, 202, 208, 237, 78, 65, 84, 186, 243, 200, 207, 214, 164]
a = ''.join([struct.pack('B', i) for i in a]).decode('gbk')
print a