import time
import board
import analogio
import digitalio
import usb_cdc
import array

btna = digitalio.DigitalInOut(board.BUTTON_A)
btnb = digitalio.DigitalInOut(board.BUTTON_B)
downThreshold = 900
upThreshold = 1200
light = analogio.AnalogIn(board.LIGHT)
t0 = 0
usb_cdc.data.write(array.array('H',[123,456]))
usb_cdc.data.write(array.array('Q',[789, 123]))
while True:
    lv = light.value
    while lv > downThreshold:
        lv = light.value
    t1 = time.monotonic_ns()
    lv0 = lv
    while lv < upThreshold:
        lv = light.value
    usb_cdc.data.write(array.array('H',[lv0,lv]))
    usb_cdc.data.write(array.array('Q',[t0, t1]))
    print(lv0,lv,t0,t1)
    t0 = t1
