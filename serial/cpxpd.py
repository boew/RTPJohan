#!/usr/bin/python3.9 
import datetime as dt
import serial
import sys
import struct
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

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
            maxCount = struct.calcsize('HHQQ')
            while (bytes([cs]) != cr):
                cr = sp.read()
                maxCount -= 1
                if (0 >= maxCount):
                    sys.exit('Oooops - startSync failed!')

    def doLog(idx, td):
        msg = dt.datetime.now().strftime(formatString)
        msg += "; " + str(idx) + ", " + str(td)
        with open('cpxpd_log.txt', 'a') as logfile:
            print(msg, file=logfile)

    def mPlot():
        tmpPath = Path('../test/tmp_mplot.svg')
        realPath = Path('../test/mplot.svg')
        srmplt = sr_m.plot()
        srmpltTitle  = 'mplot '
        srmpltTitle += dt.datetime.now().strftime(formatString)
        print(srmpltTitle)
        srmplt.set_title(srmpltTitle)
        plt.savefig(tmpPath)
        plt.cla()
        tmpPath.replace(realPath)

    def hPlot():
        tmpPath = Path('../test/tmp_hplot.svg')
        realPath = Path('../test/hplot.svg')
        srhplt = sr_h.plot()
        srhpltTitle  = 'hplot '
        srhpltTitle += dt.datetime.now().strftime(formatString)
        print(srhpltTitle)        
        srhplt.set_title(srhpltTitle)
        plt.savefig(tmpPath)
        plt.cla()
        tmpPath.replace(realPath)

    def dPlot():
        tmpPath = Path('../test/tmp_dplot.svg')
        realPath = Path('../test/dplot.svg')
        srdplt = sr_d.plot()
        srdpltTitle  = 'dplot '
        srdpltTitle += dt.datetime.now().strftime(formatString)
        print(srdpltTitle)        
        srdplt.set_title(srdpltTitle)
        plt.savefig(tmpPath)
        plt.cla()
        tmpPath.replace(realPath)

    m_max = 16 #16 
    h_max = 45 #45
    d_max = 24
    sr_m = pd.Series([0.0]* m_max)         # 16 * ~5s <-> ~80 s
    sr_h = pd.Series([0.0]* h_max)         # 45 * ~80 s <-> ~1 h
    sr_d = pd.Series([0.0]* d_max)         # 24 * ~1 h <-> ~1 day
    m_index=0
    h_index=0
    d_index=0
    m_filled = False
    print(f'{sys.argv[0]} @ {dt.datetime.now().strftime("%Y-%m-%d; %H:%M:%S")}')
    with serial.Serial('/dev/ttyACM1', 115200) as sPort:
        print('before syncOrExit')
        syncOrExit(sPort)
        print('after syncOrExit ')
        while True:
            r0 = sPort.read(8)
            (tns0,) = struct.unpack('Q', r0)
            r1 = sPort.read(8)
            (tns1,) = struct.unpack('Q', r1)
            td = (tns1 - tns0) // 1000000 # ns to ms
            sr_m[m_index] = td / 1000
            m_index += 1
            m_index %= m_max
            if (0 == m_index):
                sr_h[h_index] = sr_m.mean()
                mPlot()
                doLog(h_index, sr_h[h_index])
                h_index += 1
                h_index %= h_max
                if (0 == h_index):
                    sr_d[d_index] = sr_h.mean()
                    hPlot()
                    d_index += 1
                    d_index %= d_max

                
                
# if ('__main__' == __name__) :
#     # if (2 > len(sys.argv)):
#     #     print(f'Usage: {sys.argv[0]} On|Off ') 
#     #     sys.exit(-1)
#     # else:
#     #     print(f'Yaaaaay: {sys.argv}')         
#     main()
