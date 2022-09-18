import sys
print(sys.path)
sys.path.append('../serial')
import mhdTracker as MT

#if '__main__' == __name__ :
if True:
    mT=MT.MhdTracker('m', 16, pathParts=['../test/','plot.svg'])       
    for i in range(16):
        print(mT.update(i, i*3))
    print(mT.series)
    mT.doPlot()
