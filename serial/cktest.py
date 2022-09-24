#!/usr/bin/python3.9 
import sys
import struct

with open('mktest2.txt', 'rb') as binaryFile:
    bfd = binaryFile.read()
    while (16 <= len(bfd)):
        blink=bfd[:16]
        bfd = bfd[16:]
        (tns0,tns1) = struct.unpack('QQ',blink)
        print(tns0,tns1, (tns1-tns0) / 1e9)
        
        
