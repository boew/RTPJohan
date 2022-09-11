import time
import board
import analogio

downThreshold = 900
upThreshold = 1200
light = analogio.AnalogIn(board.LIGHT)

print(light.value)
while True:
    tid_ljus=[]
    lv = light.value
    while lv > downThreshold:
        lv = light.value
    tid_ljus.append((lv, time.monotonic()))
    while lv < upThreshold:
        lv = light.value
    tid_ljus.append((lv, time.monotonic()))
    print(tid_ljus)
