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
usb_cdc.data.write(array.array('H',[123,456]))
while True:
    lv = light.value
    while lv > downThreshold:
        lv = light.value
        if (btna.value or btnb.value):
            break
    lv0 = lv
    while lv < upThreshold:
        lv = light.value
        if (btna.value or btnb.value):
            break
    usb_cdc.data.write(array.array('H',[lv0,lv]))
    print(btna.value,btnb.value,time.monotonic())
