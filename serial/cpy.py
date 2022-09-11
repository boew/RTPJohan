#!/usr/bin/python3.9 
import datetime
import serial
import sys

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
    with serial.Serial('/dev/ttyACM0', 115200, timeout=60) as sPort:
        while True:
            oneLine = sPort.readline()
            doLog(datetime.datetime.now(), oneLine)
                
                
if ('__main__' == __name__) :
    # if (2 > len(sys.argv)):
    #     print(f'Usage: {sys.argv[0]} On|Off ') 
    #     sys.exit(-1)
    # else:
    #     print(f'Yaaaaay: {sys.argv}')         
    main()
