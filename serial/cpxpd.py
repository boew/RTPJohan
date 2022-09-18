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

    def mPlot():
        tmpPath = Path('../test/tmp_mplot.svg')
        realPath = Path('../test/mplot.svg')
        srmplt = sr_m.plot()
        titleTime = mhd_t0 + dt.timedelta(milliseconds = m_acc_ns // 1e6)
        srmpltTitle  = 'mplot ' + titleTime.strftime(formatString)
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
        srhpltTitle += (mhd_t0 + h_acc_ns / 1e9 ).strftime(formatString)
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
        srdpltTitle += (mhd_t0 + d_acc_ns / 1e9 ).strftime(formatString)
        print(srdpltTitle)        
        srdplt.set_title(srdpltTitle)
        plt.savefig(tmpPath)
        plt.cla()
        tmpPath.replace(realPath)

    m_max = 16 #16 
    h_max = 45 #45
    d_max = 24
    sr_m = pd.Series([0]* m_max)         # 16 * ~5s <-> ~80 s
    sr_h = pd.Series([0]* h_max)         # 45 * ~80 s <-> ~1 h
    sr_d = pd.Series([0]* d_max)         # 24 * ~1 h <-> ~1 day
    m_index= 0
    h_index = 0
    d_index = 0
    m_acc_ns = 0 
    h_acc_ns = 0 
    d_acc_ns = 0 
    print(f'{sys.argv[0]} @ {dt.datetime.now().strftime("%Y-%m-%d; %H:%M:%S")}')
    with serial.Serial('/dev/ttyACM1', 115200) as sPort:
        print('before syncOrExit')
        syncOrExit(sPort)
        print('after syncOrExit ')
        mhd_t0 = None
        while True:
            (tns0,tns1) = struct.unpack('QQ', sPort.read(16))
            if (not mhd_t0):
                mhd_t0 = dt.datetime.now()
            sr_m[m_index] = tns1 - tns0
            m_index += 1
            m_index %= m_max
            if (0 == m_index):
                m_acc_ns += sr_m.sum()
                mPlot()
                sr_h[h_index] = sr_m.mean()
                doLog(h_index, sr_h[h_index])
                h_index += 1
                h_index %= h_max
                if (0 == h_index):
                    h_acc_ns += sr_h.sum()
                    hPlot()
                    sr_d[d_index] = sr_h.mean()
                    d_index += 1
                    d_index %= d_max
                    if (0 == d_index):
                        d_acc_ns += sr_d.sum()
                        dPlot()
                        d_index += 1
                        d_index %= d_max

                
                
# if ('__main__' == __name__) :
#     # if (2 > len(sys.argv)):
#     #     print(f'Usage: {sys.argv[0]} On|Off ') 
#     #     sys.exit(-1)
#     # else:
#     #     print(f'Yaaaaay: {sys.argv}')         
#     main()
