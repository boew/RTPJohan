import matplotlib.pyplot as plt
import pandas as pd
import time
from pathlib import Path
import random
import datetime as dt
tmppath = Path('tmp_line.svg')
realpath = Path('line.svg')

def ns2P(ns):
    return 3.6 * 1e9 / ns

def ns2dt(ns):
    return mhd_t0 + dt.timedelta(milliseconds = ns // 1e6)

if True:
    r = 16
    mhd_t0 = dt.datetime.now()
    mhd_ns_acc = 0
    print(r)
    #xs = list(range(r))
    #for x in range(r):
    #    xs[x] = random.randint(4e9,6e9)
    xs = [4497295185, 4862322240, 4312131602, 4574300305, 5393615637, 5996208421, 4259335093, 5012602027, 4188253323, 5433751451, 5089688769, 5241195772, 4491990920, 4974666319, 5473096180, 4147844358]
    sr = pd.Series(xs)
    sdf = pd.DataFrame({'sr': sr, 'srdt': map(ns2dt, sr.cumsum()), 'srP': map(ns2P, sr)})
    #sdf.plot('srdt','srP', marker='x')
    sdf.plot('srdt','srP', kind='bar')
    #sr.plot()
    plt.show()
    #plt.savefig(tmppath)
    #tmppath.replace(realpath)
    #time.sleep(2)

#for r in range(2,16):
#    doStuff(r)

#for r in range(16,2,-1):
#    doStuff(r)

