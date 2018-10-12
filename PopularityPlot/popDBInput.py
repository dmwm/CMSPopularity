#!/usr/bin/env python

# system modules
import os
import json
import cPickle

# local modules
from inputs import loadOptions
# load options first since they define all inputs parameters
if __name__ == '__main__':
    loadOptions()
from inputs import baseDir, outputDir, testDS
from utils import fopen
from utils import dStarts, dEnd, getDatePop
from dbsInput import readDBSInfo

def savePopDB(dbsInfo):
    #read in the popularity jsons
    myF = fopen(os.path.join(baseDir, 'popDaily.txt'))

    myJInput=''
    for line in myF:
        myJInput += line

    myJ=json.loads(myJInput)

    dates=myJ.keys()

    #make a dictionary of datasets on disk during the various time intervals
    #divide the number of accesses for each dataset by the number of files in the dataset
    #summing up accesses on all days during the interval.
    #TODO: Protect against data in the popularity jsons that is after the end date of the plot
    datasets={}
    datasetDetails={}
    startKeys=dStarts.keys()
    for dateStart in startKeys:
        datasets[dateStart]={}

    for d in dates:
        dVal=getDatePop(d)
        
        records=myJ[d]['DATA']

        for record in records:
            dataset=record["COLLNAME"]
            if dataset == testDS:
                print 'Dataset read',d,record["NACC"]
            if dataset not in dbsInfo:
                continue
            if 'num_files' in dbsInfo[dataset]:
                nFiles=dbsInfo[dataset]['num_files']
            else:
                nFiles=dbsInfo[dataset]['nfiles']

            if dataset not in datasetDetails:
                datasetDetails[dataset]={}
            datasetDetails[dataset][dVal]=datasetDetails[dataset].get(dVal,0)+ float(record["NACC"])/float(nFiles)

            for dateStart in startKeys:
                if dVal>=dStarts[dateStart] and dVal <=dEnd:
                    datasets[dateStart][dataset] = datasets[dateStart].get(dataset,0) + float(record["NACC"])/float(nFiles)
    #some printout
    for dateStart in startKeys:
        print len(datasets[dateStart].keys())        

    print "popularity for",testDS
    for dateStart in startKeys:
        print dateStart+" :", datasets[dateStart].get(testDS,0)

    fp = fopen(os.path.join(outputDir, 'popDBDetails.data.gz'), 'wb')
    cPickle.dump(datasetDetails, fp)
    fp.close()

def readPopDB():
    "Read PopDB data and return back datasets dict"
    fp = fopen(os.path.join(outputDir, 'popDBDetails.data.gz'), 'rb')
    datasets = cPickle.load(fp)
    fp.close()
    return datasets

if __name__ == '__main__':
    savePopDB(readDBSInfo())
