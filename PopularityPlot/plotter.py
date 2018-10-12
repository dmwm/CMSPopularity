#!/usr/bin/env python

# system modules
import os

# numpy and matplotlib
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as  pylab

# local modules
from inputs import outputDir
from utils import fopen

def plotPopularity(arr, keys, popSource, dataLoc, figNum, iformat='png'):

    xVals=numpy.arange(len(arr))
    yByCount=numpy.zeros(len(arr))
    yBySizes={}
    knownTimes={}
    knownSamples={}
    for key in keys:
        yBySizes[key]=numpy.zeros(len(arr))
        sp=key.split()
        knownTimes[sp[0]]=1
        knownSamples[sp[1]]=1

    for i,a in enumerate(arr):
        yByCount[i]=(a[0])
        for j,key in enumerate(keys):
            yBySizes[key][i]=a[j+1]

    width=0.25
    figNum=figNum+1
    pylab.figure(figNum)
    pylab.bar(xVals,yByCount,width,color='r')
    
    pylab.xlabel('Number of accesses',fontsize=15)
    pylab.ylabel('Number of collections',fontsize=15)
    fname = os.path.join(outputDir, "plots/popNum_"+popSource+" "+dataLoc)
    if not os.path.isdir(os.path.join(outputDir, "plots")):
        os.makedirs(os.path.join(outputDir, "plots"))
    pylab.savefig(fname + '.' + iformat, format=iformat)
    pylab.ylim(0,numpy.amax(yByCount)*1.1)
    ax=pylab.gca()
    ax.set_xticks(xVals+width/2.)
    ax.set_xticklabels(xVals)

    figNum=figNum+1
    cols=['r','g','b']
    for sample in knownSamples:

        figNum=figNum+1
        pylab.figure(figNum)
        nBars=0
        tMaxes=numpy.zeros(len(knownTimes.keys()))
        plottedKeys=[]
        for key in keys:
            sp=key.split()
            if sp[1]!= sample:
                continue
            nMonths=sp[0]
            plottedKeys.append(key)
            print yBySizes[key]
            print "Sum",key,sample,popSource,dataLoc,numpy.sum(yBySizes[key])
            
            pylab.bar(xVals+nBars*width,yBySizes[key],width,color=cols[nBars],label=nMonths+" months, sum="+"{0:.1f}".format(numpy.sum(yBySizes[key])))
            tMaxes[nBars]=numpy.amax(yBySizes[key])
            nBars=nBars+1


        pylab.xlabel('Number of accesses',fontsize=15)
        pylab.ylabel('Weighted total size',fontsize=15)

        pylab.ylim(0,numpy.amax(tMaxes)*1.1)
        pylab.xlim(0,xVals[-1]+1)
        ax=pylab.gca()
        ax.set_xticks(xVals+width*1.5)
        xLabels=["0 Old"]
        for i in range(len(xVals)-2):
            xLabels.append(str(i))
        xLabels.append(str(len(xVals)-2)+"+")

        ax.set_xticklabels(xLabels)
#        ax.set_xticklabels(xVals)
        pylab.legend(loc='best')
        pylab.title("Samples considered: "+sample+", popData="+popSource+" data GID="+dataLoc)
        fname = os.path.join(outputDir, "plots/popSize_"+sample+"_"+popSource+"_"+dataLoc)
        if not os.path.isdir(os.path.join(outputDir, "plots")):
            os.makedirs(os.path.join(outputDir, "plots"))
        pylab.savefig(fname + '.' + iformat, format=iformat)

        fname = os.path.join(outputDir, "data/popSize_"+sample+"_"+popSource+"_"+dataLoc+'.csv.gz')
        if not os.path.isdir(os.path.join(outputDir, "data")):
            os.makedirs(os.path.join(outputDir, "data"))
        fH = fopen(fname, 'w')
#        fH = fopen(os.path.join(outputDir, "popSize_"+sample+"_"+popSource+"_"+dataLoc+'.csv.gz'),'w')
        
        fH.write('NAccesses')
        for key in plottedKeys:
            sp=key.split()
            fH.write(','+sp[0]+' months (PB)')
        fH.write('\n')
        for k in range(len(xVals)):
            fH.write(str(xLabels[k]))
            for key in plottedKeys:
                fH.write(','+str(yBySizes[key][k]))
            fH.write('\n')
        fH.close()
    return figNum



if __name__ == "__main__":

    plot( [ [100,10.,5.,2.],[5,1.,0.5,0.5],[20,3.,2.,1.],[40,20.,10.,5.]],["3 All","6 All","12 All"],"test")
    pylab.show()
