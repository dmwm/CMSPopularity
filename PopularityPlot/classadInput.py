#!/usr/bin/env python

# system modules
import os
import cPickle
import datetime
 
# local modules
from inputs import loadOptions
# load options first since they define all inputs parameters
if __name__ == '__main__':
    loadOptions()
from inputs import baseDir, outputDir, classAdsInput
from dbsInput import readDBSInfo
from utils import dStarts, dEnd, fopen

def saveClassAds(dbsInfo):
    "Generate class ads information and save it on disk"
    datasets = {}
    datasetDetails = {}
    startKeys = dStarts.keys()
    for dateStart in startKeys:
        datasets[dateStart] = {}

    print("### use classAdsInput %s" % classAdsInput)

    for root, dirs, files in os.walk(classAdsInput, topdown = False):
        for idx, name in enumerate(sorted(files)):
            nNull = 0
            nNonNull = 0
            nNullEvts = 0
            fName = os.path.join(root, name)
            headers = []
            skip = False
            with fopen(fName, 'rb') as istream:
                for line in istream:
                    sp = line.split(',')
                    if not headers:
                        headers = sp
                        continue
                    # check if it is dataset-YYYYMMDD.csv file
                    check = ('sum_evts' in headers) or\
                            ('num_events' in headers) or\
                            ('nevents' in headers)
                    if not check:
                        print("Skip %s" % fName)
                        skip = True
                        break
                    if len(sp) < 6:
                        continue
                    if sp[0]  ==  "null": 
                        nNull += 1
                        continue
                    if sp[6] == "null":
                        nNullEvts += 1
                        continue
                    if sp[0]  ==  "dataset": continue
                    nNonNull += 1
                    try:
                        ts = long(sp[5])
                    except:
                        continue
                    if ts > 25180904520: #its in milliseconds!
                        ts = long(ts/1000)
                    #there are also bogus timestamps - some are easy to recover
                    while ts > 25180904520: 
			ts = long(ts/1000)   
                    try:
                        dVal = datetime.datetime.fromtimestamp(ts).date()#getDate(sp[8])
                    except ValueError:
                        print 'skipping bad timestamp',ts,line
                        continue 
                    dataset = sp[0]
                    if "/DQMIO" in dataset:
                        continue #there are no events...
                    if dataset not in dbsInfo:
                        continue
                    if 'num_events' in dbsInfo[dataset]:
                        nEvts = dbsInfo[dataset]["num_events"]
                    elif 'nevents' in dbsInfo[dataset]:
                        nEvts = dbsInfo[dataset]["nevents"]
                    elif 'sum_evts' in dbsInfo[dataset]:
                        nEvts = dbsInfo[dataset]["sum_evts"]
                    if float(nEvts)<1:
                        nEvts = 1.
                    if dataset not in datasetDetails:
                        datasetDetails[dataset] = {}
                    datasetDetails[dataset][dVal] = datasetDetails[dataset].get(dVal,0)+ float(sp[6])*1000/float(nEvts)  

                    for dateStart in startKeys:
                        if dVal >= dStarts[dateStart] and dVal <= dEnd:
                            datasets[dateStart][dataset] = datasets[dateStart].get(dataset,0) + float(sp[6])*1000/float(nEvts)


            if not skip:
                try:
                    print("%3d %s %s %s" % (idx, name, nNull/float(nNonNull+nNull+nNullEvts+1e-5), nNullEvts/float(nNonNull+nNull+nNullEvts+1e-5)))
                except:
                    pass

    #make a dictionary of datasets on disk during the various time intervals
    #divide the number of accesses for each dataset by the number of files in the dataset
    #summing up accesses on all days during the interval.
    #TODO: Protect against data in the popularity jsons that is after the end date of the plot

    fp = fopen(os.path.join(outputDir, 'classads.data.gz'), 'wb')
    cPickle.dump(datasets,fp)
    fp.close()

    fp = fopen(os.path.join(outputDir, 'classadsDetails.data.gz'), 'wb')
    cPickle.dump(datasetDetails,fp)
    fp.close()

def readClassAds():
    "Read class ads data and return back datasets dict"
    fp = fopen(os.path.join(outputDir, 'classads.data.gz'), 'rb')
    datasets = cPickle.load(fp)
    fp.close()
    return datasets

if __name__ == '__main__':
    saveClassAds(readDBSInfo())
