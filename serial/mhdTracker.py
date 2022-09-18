import pandas as pd
import datetime as dt
from pathlib import Path
import matplotlib.pyplot as plt

class MhdTracker:
    """
    """
    mhd_t0 = None
    def __init__(self, x, iMax, pathParts=['../web/', 'plot.svg'] ):
        self.x = x
        self.tmpPath = Path(f'{pathParts[0]}tmp_{x}{pathParts[1]}')
        self.realPath = Path(f'{pathParts[0]}{x}{pathParts[1]}') 
        self.iMax=iMax
        self.i=0
        self.acc_ns=0
        self.acc_cnt=0 
        self.series=pd.Series([0] * self.iMax)
        self.formatString = "%Y-%m-%d %H:%M:%S"
        # 2022-09-11 12:12:01
        #    Y  m  d  H  M  S    

        

    def update(self, tnsDiff):
        if (not MhdTracker.mhd_t0):
            MhdTracker.mhd_t0 = dt.datetime.now()
        self.series[self.i] = tnsDiff
        self.i += 1
        self.i %= self.iMax
        if (0 == self.i):
            self.acc_ns += self.series.sum()
            self.acc_cnt += 1
        return (0 == self.i)
        
    def doPlot(self, toFile=False):
        self.plot = self.series.plot()
        self.tTime = MhdTracker.mhd_t0 + dt.timedelta(milliseconds = self.acc_ns // 1e6)
        self.pTitle  = f'{self.x}plot {self.acc_cnt % self.iMax}/({self.iMax}) @ '
        self.pTitle += self.tTime.strftime(self.formatString)
        print(self.pTitle)
        self.plot.set_title(self.pTitle)
        if (toFile):
            plt.savefig(self.tmpPath)
            plt.cla()
            self.tmpPath.replace(self.realPath)
        else:
            plt.show()

if '__main__' == __name__ :
    mT=MhdTracker('m', 16, pathParts=['../test/','plot.svg'])       
    for i in range(16):
        print(mT.update(i*3-i))
    print(mT.series)
    mT.doPlot()
