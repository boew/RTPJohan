#!/usr/bin/python3.9 
import datetime as dt
import serial
import sys
import struct
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
    
#def main():
if True:
    def doLog(p1,p2):
        formatString = "%Y-%m-%d; %H:%M:%S"
        # 2022-09-11	12:12:01
        #    Y  m  d         H  M  S
        msg = dt.datetime.now().strftime(formatString)
        msg += "; " + str(p1) + str(p2)
        with open('cpxpd_log.txt', 'a') as logfile:
            print(msg, file=logfile)

    def doPlot():
        tmpPath = Path('tmp_line.svg')
        realPath = Path('line.svg')
        formatString = "%Y-%m-%d %H:%M:%S"
        # 2022-09-11	12:12:01
        #    Y  m  d         H  M  S    
        srhplt = sr_h.plot()
        srhpltTitle = dt.datetime.now().strftime(formatString)
        # print(srhpltTitle[:8])
        # print(srhpltTitle[8])
        # print(srhpltTitle[9])
        # print(srhpltTitle[10:])
        srhplt.set_title(srhpltTitle)
        plt.savefig(tmpPath)
        plt.cla()
        tmpPath.replace(realPath)
    m_max = 4 #16
    h_max = 45
    d_max = 24
    sr_m = pd.Series([0.0]* m_max)         # 16 * ~5s <-> ~80 s
    sr_h = pd.Series([0.0]* h_max)         # 45 * ~80 s <-> ~1 h
    sr_d = pd.Series([0.0]* d_max)         # 24 * ~1 h <-> ~1 day
    m_index=0
    h_index=0
    d_index=0
    t00 = False
    m_filled = False
    with serial.Serial('/dev/ttyACM1', 115200, timeout=60) as sPort:
        while True:
            r0 = sPort.read(2)
            t0 = dt.datetime.now()
            r1 = sPort.read(2)
            t1 = dt.datetime.now()
            if (t00):
                sr_m[m_index]  = (t0 - t00).seconds 
                sr_m[m_index] += (t0 - t00).microseconds / 1000000
                m_index += 1
                m_index %= m_max
                if (0 == m_index):
                    sr_h[h_index] = sr_m.mean()
                    doPlot()
                    doLog(h_index, sr_h[h_index] )
                    h_index += 1
                    h_index %= h_max
                    if (0 == h_index):
                        sr_d[d_index] = sr_h.mean()
                        d_index += 1
                        d_index %= d_max
            t00 = t0
                
                
# if ('__main__' == __name__) :
#     # if (2 > len(sys.argv)):
#     #     print(f'Usage: {sys.argv[0]} On|Off ') 
#     #     sys.exit(-1)
#     # else:
#     #     print(f'Yaaaaay: {sys.argv}')         
#     main()
