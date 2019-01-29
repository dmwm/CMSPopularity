#!/usr/bin/env python

# system modules
import os
import sys
import argparse

###
### Changes to intervals, intervalStartStrings, intervalEndString, phedexDataFile
### parameters mean that the script phedexMeans.py should be rerun to get correct results

# base location for writing output and finding input
baseDir = '/data/cms/pop-data' # area on vocms0130
outputDir = os.path.join(os.getcwd(), 'output')

#interested in 3 6 and 12 months
intervals = ['3','6','12']
intervalStartStrings = {'3':'20171001','6':'20170701','12':'20170101'}
intervalEndString = '20180131'

#where to get the popularity data from (which python to import)
#popularitySource = "popDB"
popularitySource = "classads"

# location of dataset df's (aka classAdds from dbs+condor joins)
#classAdsInput = os.path.join(baseDir, 'datasets')
classAdsInput = os.path.join(baseDir, 'dbs_condor')

dbsInput = os.path.join(baseDir, "dbs_events.csv.gz")
#dbsFormat = "mine"
dbsFormat = "hadoop"

#which phedex dump to use
#phedexDataFile = os.path.join(baseDir, "phedex_20170101_20180131.csv.gz")
phedexDataFile = os.path.join(baseDir, "phedex/phedex_20170901_20180831.csv.gz")
loadPhedexMeans = False
loadClassAds = False
loadPopDB = False

# a label to apply to all plots
isTest = False
iformat = 'pdf'

#some datasets to use for testing
testDS = "/ZprimeToTT_M-2500_W-250_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"

#the end of the popularity plot
maxPop = 15

#divide the number of dataset accesses by the average number of copies or not?
#eg, divide the value on the x axis.. for the moment no
divideByNCopies = False

# data types to produce
dataTypes= ['All','AOD','AODSIM','MINIAOD','MINIAODSIM',
            'sAODs','Upgrade','RECO','GENSIMRECO',
            'GENSIMRAW','RAW','ALCARECO','Other',
            'GENSIM','GEN','LHE','USER',
            'FEVT','PREMIXRAW','RAWAODSIM','DQMIO',
            'GENSIMRECODEBUG','GENRAW','RAWRECO']

use_only_tier2=False

### DO NOT EDIT BELOW THIS LINE

class OptionParser():
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--baseDir", action="store",
            dest="baseDir", default=baseDir, help="Input directory with data, default %s" % baseDir)
        odir = os.path.join(os.getcwd(), 'output')
        self.parser.add_argument("--outputDir", action="store",
            dest="outputDir", default=odir, help="Output directory to store results, default %s" % odir)
        self.parser.add_argument("--phedexInput", action="store",
            dest="phedexInput", default=phedexDataFile, help="input PhEDEx data file, default %s" % phedexDataFile)
        self.parser.add_argument("--dbsInput", action="store",
            dest="dbsInput", default=dbsInput, help="input DBS data file, default %s" % dbsInput)
        self.parser.add_argument("--classAdsInput", action="store",
            dest="classAdsInput", default=classAdsInput, help="classAdsInput data area, default %s" % classAdsInput)
        self.parser.add_argument("--popularitySource", action="store",
            dest="popularitySource", default=popularitySource, help="popularity input type, default classads")
        intervals = ','.join([str(i) for i in sorted([int(i) for i in intervalStartStrings.keys()])])
        self.parser.add_argument("--intervals", action="store",
            dest="intervals", default=intervals, help="Date intervals to use, default %s" % intervals)
        dates = ','.join([str(i) for i in reversed(sorted([int(i) for i in intervalStartStrings.values()]))])
        self.parser.add_argument("--intervalDates", action="store",
            dest="intervalDates", default=dates,
            help="Date intervalDates to use, default %s" % dates)
        self.parser.add_argument("--intervalEnd", action="store",
            dest="intervalEnd", default=intervalEndString,
            help="End date for intervals to use, default %s" % intervalEndString)
        self.parser.add_argument("--loadPhedexMeans", action="store_true",
            dest="loadPhedexMeans", default=False, help="load PhEDEx means from output dir")
        self.parser.add_argument("--loadClassAds", action="store_true",
            dest="loadClassAds", default=False, help="Load classads from output dir")
        self.parser.add_argument("--loadPopDB", action="store_true",
            dest="loadPopDB", default=False, help="Load popDB from output dir")
        self.parser.add_argument("--maxPop", action="store",
            dest="maxPop", default=maxPop, help="Input directory with data")
        self.parser.add_argument("--testDS", action="store",
            dest="testDS", default=testDS, help="Test dataset")
        self.parser.add_argument("--dataTypes", action="store",
            dest="dataTypes", default="", help="comma separated list of data-tiers to produce")
        self.parser.add_argument("--divideByNCopies", action="store_true",
            dest="divideByNCopies", default=False, help="Divide #datasets access by avg number of copies")
        self.parser.add_argument("--iformat", action="store",
            dest="iformat", default=iformat, help="Image format, default png")
        self.parser.add_argument("--useOnlyTier2", action="store_true",
            dest="use_only_tier2", default=False, help="Phedex data only on tier-2 rather than tier-1+tier-2, default False")

def loadOptions():
    "Load all options"
    optmgr  = OptionParser()
    opts = optmgr.parser.parse_args()

    global baseDir, outputDir, loadPhedexMeans, loadClassAds, intervals, testDS, maxPop
    global phedexDataFile, dbsInput, popularitySource, loadPopDB, iformat
    global classAdsInput, intervalStartStrings, intervalEndString, dataTypes

    baseDir = opts.baseDir
    outputDir = opts.outputDir
    loadPhedexMeans = opts.loadPhedexMeans
    loadClassAds = opts.loadClassAds
    loadPopDB = opts.loadPopDB
    classAdsInput = opts.classAdsInput
    intervals = opts.intervals.split(',') if opts.intervals else intervals
    intervalDates = opts.intervalDates.split(',')
    if intervalDates:
        intervalStartStrings = dict(zip(intervals, intervalDates))
    intervalDates = intervalStartStrings
    intervalEndString = opts.intervalEnd
    testDS = opts.testDS
    if opts.dataTypes:
        dataTypes = opts.dataTypes.split(',')
    maxPop = opts.maxPop
    phedexDataFile = opts.phedexInput
    popularitySource = opts.popularitySource
    dbsInput = opts.dbsInput
    iformat = opts.iformat
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

