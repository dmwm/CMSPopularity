#!/usr/bin/env python

# system modules
import os
import cPickle

# local modules
from inputs import loadOptions
# load options first since they define all inputs parameters
if __name__ == '__main__':
    loadOptions()
from inputs import intervalStartStrings, intervalEndString, outputDir
from utils import fopen
from phedexInput import readSizes

# read in from files or recreate the mean size on T1/T2disk for each dataset
# to recreate the files, call this python script directory.
# to read from disk, just import effectiveMeans(AnaOps,AllOps) directly in your script

# TODO - put the three dictionaries into an array to reduce code
# TODO - key the data files on start and stop dates to ensure there is no mismatch in data
def recreate():

    #these are time intervals of interest
    from utils import nDaysDict

    #read in the detailed information from the phedex dumps
    effectiveSizesDict = readSizes()
#    from phedexInput import effectiveSizesDict#,effectiveSizesAnaOps,effectiveSizesCompOps
    keysES=effectiveSizesDict.keys()
    import numpy
    effectiveMeansDict={}
    keys=nDaysDict.keys()
    for keyES,cached in effectiveSizesDict.iteritems():
        cachedOut={}
        for dataset,es in cached.iteritems():
            cachedOut[dataset]={ k: numpy.mean(es[-1*nDaysDict[k]:]) for k in keys}
        #these are the outputs
        effectiveMeansDict[keyES]=cachedOut
    #done - now save them to disk
    return effectiveMeansDict

def savePhedexMeans():
    "Save effectirMeansDict to disk"
    effectiveMeansDict=recreate()
    key=intervalStartStrings['12']+'_'+intervalEndString

    keysES=effectiveMeansDict.keys()
    for keyES in keysES:
        fname = os.path.join(outputDir, 'effectiveMeans'+keyES+'_'+key+'.data.gz')
        print("writing %s: %s" % (keyES, fname))
        fp = fopen(fname, 'wb')
        cPickle.dump(effectiveMeansDict[keyES],fp)
        fp.close()

def readPhedexMeans():
    "Initialize effectiveMeansDict from data on disk"
    #read in the stored information from disk
    key=intervalStartStrings['12']+'_'+intervalEndString

    keysES=["All", "AnaOps", "AllOps", "MinusOne"]

    effectiveMeansDict = {}
    for keyES in keysES:
        fname = os.path.join(outputDir, 'effectiveMeans'+keyES+'_'+key+'.data.gz')
        print("reading %s: %s" % (keyES, fname))
        fp = fopen(fname, 'rb')
        effectiveMeansDict[keyES]=cPickle.load(fp)
        fp.close()
    return effectiveMeansDict

if __name__ == "__main__":
    savePhedexMeans()
