import pandas as pd
import datetime as dt
from pathlib import Path
import matplotlib.pyplot as plt

class MhdTracker:
    """
    """
    mhd_t0 = False
    def __init__(self, x, iMax):
        self.x = x
        self.tmpPath = Path(f'../test/tmp_{x}plot.svg')
        self.realPath = Path(f'../test/{x}plot.svg')
        self.iMax=iMax
        self.i=0
        self.acc_ns=0
        self.series=pd.Series([0] * self.iMax)
        self.formatString = "%Y-%m-%d %H:%M:%S"
        # 2022-09-11 12:12:01
        #    Y  m  d  H  M  S    

        

    def update(self, tns0, tns1):
        if (not MhdTracker.mhd_t0):
            MhdTracker.mhd_t0 = dt.datetime.now()
        self.series[self.i] = tns1 - tns0
        self.i += 1
        self.i %= self.iMax
        if (0 == self.i):
            self.acc_ns += self.series.sum()
        return (0 == self.i)
        
    def doPlot(self):
        self.plot = self.series.plot()
        self.tTime = MhdTracker.mhd_t0 + dt.timedelta(milliseconds = self.acc_ns // 1e6)
        self.pTitle  = f'{self.x}plot ' + self.tTime.strftime(self.formatString)
        print(self.pTitle)
        self.plot.set_title(self.pTitle)
        plt.show()
        #plt.savefig(tmpPath)
        #plt.cla()
        #tmpPath.replace(realPath)


if True:
    mT=MhdTracker('m',16)       # 16 * ~5s <-> ~80 s  
    hT=MhdTracker('m',45)       # 45 * ~80 s <-> ~1 h 
    dT=MhdTracker('m',24)       # 24 * ~1 h <-> ~1 day
    for i in range(16):
        print(mT.update(i, i*3))
    
