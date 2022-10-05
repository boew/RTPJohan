#!/usr/bin/python3.9 
import datetime as dt
import serial
import sys
import struct
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import mhdTracker as MT

formatString = "%Y-%m-%d; %H:%M:%S"
# 2022-09-11 12:12:01
#    Y  m  d  H  M  S    
mT = ""
tT = ""
dT = ""
def main(bintest = False, txttest = False, txtstart = ""):
    global mT
    global hT
    global dT
    #if True:
    def syncOrExit(sp):
        syncBytes = 'cpxpdStart'.encode('utf-8')
        sp.write(syncBytes)
        cr = None
        for cs in syncBytes:
            maxCount = struct.calcsize('QQ') * 10
            while (bytes([cs]) != cr):
                cr = sp.read()
                print(maxCount, bytes([cs]), cr)
                maxCount -= 1
                if (0 >= maxCount):
                    sys.exit('Oooops - startSync failed!')

    def processBlink(tns0, tns1):
        if mT.update(tns1, tns0):
            mT.doPlot(toFile=True)
            mT.doLogTxt()
            mT.doLogXlsx()
            if hT.update(mT.series.sum()):
                hT.doPlot(True)
                if dT.update(hT.series.sum()):
                    dT.doPlot(True)

    print(f'{sys.argv[0]} @ {dt.datetime.now().strftime(formatString)}')
    if bintest:
        mT = MT.MhdTracker('m', 16,  1, './')      # 16 * ~5s <-> ~80 s  
        hT = MT.MhdTracker('h', 45, 16, './')      # 45 * ~80 s <-> ~1 h 
        dT = MT.MhdTracker('d', 24, 45, './')      # 24 * ~1 h <-> ~1 day
        with open(bintest,'rb') as binaryFile:
            tt = binaryFile.read(16)
            while 16 == len(tt):
                (tns0,tns1) = struct.unpack('QQ',tt)
                print(tns0,tns1)
                processBlink(tns0,tns1)
                tt = binaryFile.read(16)
            sys.exit(0)
    elif txttest:
        mT = MT.MhdTracker('m', 16,  1, '../test/')      # 16 * ~5s <-> ~80 s  
        hT = MT.MhdTracker('h', 45, 16, '../test/')      # 45 * ~80 s <-> ~1 h 
        dT = MT.MhdTracker('d', 24, 45, '../test/')      # 24 * ~1 h <-> ~1 day
        MT.MhdTracker.mhd_t0 = txtstart
        with open(txttest,'rb') as txtFile:
            for line in txtFile:
                tnd = int(line)
                print(0,tnd)
                processBlink(0,tnd)
            sys.exit(0)
    else:
        mT = MT.MhdTracker('m', 16,  1, '../test/')      # 16 * ~5s <-> ~80 s  
        hT = MT.MhdTracker('h', 45, 16, '../test/')      # 45 * ~80 s <-> ~1 h 
        dT = MT.MhdTracker('d', 24, 45, '../test/')      # 24 * ~1 h <-> ~1 day
        with serial.Serial('/dev/ttyACM1', 115200) as sPort:
            print('before syncOrExit')
            syncOrExit(sPort)
            print('after syncOrExit ')
            while True:
                (tns0,tns1) = struct.unpack('QQ', sPort.read(16))
                processBlink(tns0,tns1)

                
if ('__main__' == __name__) :
    if (1 == len(sys.argv)):
        print(f'Normal run, input from CPX')
        main()
    elif (2 == len(sys.argv)):
        print(f'Test run, binary input from {sys.argv[1]}')
        main(bintest=sys.argv[1])
    elif (3 == len(sys.argv)):
        print(f'Test run, text input from {sys.argv[1]}, starting at {sys.argv[2]}')
        main(txttest=sys.argv[1], txtstart=dt.datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S'))
    else:
        print(f'Got {sys.argv}, no run.')
        
