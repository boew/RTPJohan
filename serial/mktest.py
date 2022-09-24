#!/usr/bin/python3.9 
import sys
import struct

def ds2ns(t):
    return t*100000000

offsetList = list(range(30,80,5)) * 4

ts = [10]
t0 = ts[0]
for i in offsetList:
    t1 = t0+i
    ts.append(t1)
    t0 = t1

ts = list(map(ds2ns, ts))

t0 = ts[0]

with open('mktest2.txt', 'wb') as binaryFile:
    for t1 in ts[1:]:
        binaryFile.write(struct.pack('QQ',t0,t1))
        print(t0*1000000000,t1*1000000000)
        t0 = t1

with open('mktest2.txt', 'rb') as binaryFile:
    bfd = binaryFile.read()
    while (16 <= len(bfd)):
        blink=bfd[:16]
        bfd = bfd[16:]
        (tns0,tns1) = struct.unpack('QQ',blink)
        print(tns0,tns1)
        
        
