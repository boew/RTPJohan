import time
import board
import analogio
import usb_cdc
import struct

syncReq = False
def syncCheck():
    global syncReq
    nRx = usb_cdc.data.in_waiting
    if (0 < nRx):
        dRx = usb_cdc.data.read(nRx)
        print('nRx', nRx,'dRx', dRx, '@', time.monotonic_ns())
        print('sC', usb_cdc.data.write(dRx))
        syncReq = True
    else:
        syncReq = False

downThreshold = 900
upThreshold = 1200
light = analogio.AnalogIn(board.LIGHT)
t0 = 0
    
while True:
    lv = light.value
    syncCheck()
    while ((lv > downThreshold) and not syncReq):
        lv = light.value
        syncCheck()
    t1 = time.monotonic_ns()
    while ((lv < upThreshold) and not syncReq):
        lv = light.value
        syncCheck()
    if (not syncReq):
        data2write = struct.pack('QQ', t0, t1)
        usb_cdc.data.write(data2write)
    print(syncReq, t0, t1)
    t0 = t1
        
        
