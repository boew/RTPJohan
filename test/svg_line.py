import matplotlib.pyplot as plt
import pandas as pd
import time
from pathlib import Path
def p2(x):
    return 2**x
tmppath = Path('tmp_line.svg')
realpath = Path('line.svg')
def doStuff(r):
    print(r)
    plt.plot(list(range(r)), list(map(p2, range(r))))
    plt.ylabel('some numbers')
    #plt.show()
    plt.savefig(tmppath)
    tmppath.replace(realpath)
    time.sleep(2)

for r in range(2,16):
    doStuff(r)

for r in range(16,2,-1):
    doStuff(r)

