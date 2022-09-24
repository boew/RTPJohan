#!/usr/bin/python3.9 
import struct

ts = [3,4,5,6]*16

t0 = ts[0]

with open('mktest.txt', 'wb') as binaryFile:
    for t1 in ts[1:]:
        binaryFile.write(struct.pack('QQ',t0*1000000000,t1*1000000000))
        print(t0*1000000000,t1*1000000000)
        t0 = t1

with open('mktest.txt', 'rb') as binaryFile:
    bfd = binaryFile.read()
    while (16 <= len(bfd)):
        
        write(struct.pack('QQ',t0*1000000000,t1*1000000000))
        print(t0*1000000000,t1*1000000000)
        t0 = t1
        
        
