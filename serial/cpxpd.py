#!/usr/bin/python3.9 
import datetime as dt
import serial
import sys
import struct
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import mhdTracker as MT

formatString = "%Y-%m-%d %H:%M:%S"
# 2022-09-11 12:12:01
#    Y  m  d  H  M  S    

#def main():
if True:
    def syncOrExit(sp):
        syncBytes = 'cpxpdStart'.encode('utf-8')
        sp.write(syncBytes)
        cr = None
        for cs in syncBytes:
            maxCount = struct.calcsize('QQ') * 10
            while (bytes([cs]) != cr):
                print(maxCount, bytes([cs]), cr)
                cr = sp.read()
                maxCount -= 1
                if (0 >= maxCount):
                    sys.exit('Oooops - startSync failed!')

    def doLog(idx, td):
        msg = dt.datetime.now().strftime(formatString)
        msg += "; " + str(idx) + ", " + str(td)
        with open('cpxpd_log.txt', 'a') as logfile:
            print(msg, file=logfile)

    mT = MT.MhdTracker('m', 2, ['../test/','plot.svg'])      # 16 * ~5s <-> ~80 s  
    hT = MT.MhdTracker('h', 3, ['../test/','plot.svg'])      # 45 * ~80 s <-> ~1 h 
    dT = MT.MhdTracker('d', 4, ['../test/','plot.svg'])      # 24 * ~1 h <-> ~1 day
    print(f'{sys.argv[0]} @ {dt.datetime.now().strftime("%Y-%m-%d; %H:%M:%S")}')
    with serial.Serial('/dev/ttyACM1', 115200) as sPort:
        print('before syncOrExit')
        syncOrExit(sPort)
        print('after syncOrExit ')
        while True:
            (tns0,tns1) = struct.unpack('QQ', sPort.read(16))
            if mT.update(tns1-tns0):
                mT.doPlot(True)
                if hT.update(mT.series.sum()):
                    hT.doPlot(True)
                    if dT.update(hT.series.sum()):
                        dT.doPlot(True)
                
# if ('__main__' == __name__) :
#     # if (2 > len(sys.argv)):
#     #     print(f'Usage: {sys.argv[0]} On|Off ') 
#     #     sys.exit(-1)
#     # else:
#     #     print(f'Yaaaaay: {sys.argv}')         
#     main()
