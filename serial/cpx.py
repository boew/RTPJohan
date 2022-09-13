#!/usr/bin/python3.9 
import datetime
import serial
import sys
import struct
import pandas as pd

def doLog(when, msg_line):
    formatString = "%Y-%m-%d\t%H:%M:%S.%f"
    # 2022-09-11	12:12:01.791869
    #    Y  m  d     H  M  S      f
    msg = when.strftime(formatString)
    msg += " \t" 
    with open('../data/log.txt', 'a') as logfile:
        print(msg, msg_line, file=logfile)
    print(msg, msg_line)

    #https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-linux
    # 115 200 bps
    # BoE: 10s timeout

def main():
    t00 = False
    ntds = 4
    tdsfilled = False
    tds = pd.Series([0.0] * ntds)
    tdsindex = 0
    with serial.Serial('/dev/ttyACM1', 115200, timeout=60) as sPort:
        msg = ""
        while True:
            r0 = sPort.read(2)
            t0 = datetime.datetime.now()
            r1 = sPort.read(2)
            t1 = datetime.datetime.now()
            if (t00):
                tds[tdsindex]  = (t0 - t00).seconds 
                tds[tdsindex] += (t0 - t00).microseconds / 1000000
                msg  = f'Värde {tdsindex + 1}/{ntds} @ '
                tdsindex += 1
                tdsindex %= ntds
                if (0 == tdsindex):
                    tdsfilled = True
                if (tdsfilled):
                    msg = f'{ntds}-medel: {tds.mean()}'
            msg += t0.strftime("%Y-%m-%d\t%H:%M:%S")
            t00 = t0
            #(lv0,) = struct.unpack('<H',r0)
            #(lv1,) = struct.unpack('<H',r1)
            print(msg)
            #print(lv0, lv1, end = '\t')
            #doLog(datetime.datetime.now(), lv0, lv1)
                
                
if ('__main__' == __name__) :
    # if (2 > len(sys.argv)):
    #     print(f'Usage: {sys.argv[0]} On|Off ') 
    #     sys.exit(-1)
    # else:
    #     print(f'Yaaaaay: {sys.argv}')         
    main()
