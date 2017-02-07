#!/usr/bin/python
'''
This function is use for decrypt or decrypt.
And the Password encoding by base64.
'''
import base64


def encrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 6 | (buffer[i] & 0x40) >> 4 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) << 2 | (
            buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 2 | (buffer[i] & 0x02) >> 1 | (buffer[i] & 0x01) << 7


def decrypt(buffer):
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] & 0x80) >> 7 | (buffer[i] & 0x40) >> 2 | (buffer[i] & 0x20) >> 2 | (buffer[i] & 0x10) >> 2 | (
            buffer[i] & 0x08) << 2 | (buffer[i] & 0x04) << 4 | (buffer[i] & 0x02) << 6 | (buffer[i] & 0x01) << 1


def encoding_pass(password):
    password = base64.encodestring(password)
    return password


def decoding_pass(password):
    password = base64.decodestring(password)
    return password
