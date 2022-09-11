import time
import board
import analogio

downThreshold = 1000
upThreshold = 1100
light = analogio.AnalogIn(board.LIGHT)

print(light.value)
while True:
    tid_ljus=[]
    for n in range(10):
        lv = light.value
        tid_ljus.append((lv,time.monotonic()))
        while lv > downThreshold:
            lv = light.value
        tid_ljus.append((lv, time.monotonic()))
        while lv < upThreshold:
            lv = light.value
        tid_ljus.append((lv, time.monotonic()))
    print(tid_ljus)
    
