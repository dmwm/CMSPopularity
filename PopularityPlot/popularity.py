#!/usr/bin/env python

# system modules
import os
import sys
from importlib import import_module

# local modules
from inputs import loadOptions
# load options first since they define all inputs parameters
if __name__ == '__main__':
    loadOptions()
from inputs import outputDir, testDS, popularitySource, loadClassAds, loadPhedexMeans
from inputs import loadPopDB, iformat, testDS
from phedexMeans import savePhedexMeans, readPhedexMeans
from dbsInput import readDBSInfo
from utils import fopen
from classadInput import readClassAds, saveClassAds
from popDBInput import readPopDB, savePopDB
from classadInput import saveClassAds

# some parameters set by the user
from inputs import maxPop,divideByNCopies

# get the list of plots to make and some helper functions
from popKeys import cbs_keys,spKeys,findAgeKey,interestingDataset

# get the output dictionaries and another helper function
from popKeys import countsBySizeDict,computeSums,dataCategories

def plots(phedexInfo, dbsInfo, classadsInfo, iformat):
    "Generate popularity plots from phedex/dbs/classads dicts"
    #file to dump dataset by dataset tallies

    fDump=fopen(os.path.join(outputDir, 'dumpIt.txt.gz'), 'w')

    keyInfos={}
    for key in cbs_keys:
        #the plot has two attributes, the time period and the data sample
        ageKey = findAgeKey(key)
        spKey=spKeys[key]
        dsKey=(spKey[0])
        keyInfos[key]=[ageKey,dsKey]


    #loop over datasets known to phedex
    for dataset in phedexInfo['All']:
        #get attributes from DBS - some data sets are missing - these
        #these tend to be test datasets
        dbsDataset = dbsInfo.get(dataset,None) #it is likely invalid data if its not here

        # here dataset is like /GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/GEN-SIM-RAW
        # and dbsDataset is {'nfiles': 3199.0, 'nevents': 205484.0, 'size': 309328826257.0}
        if dbsDataset is not None:
            if 'creation_date' not in dbsDataset:
                continue
            ageDataset = dbsDataset['creation_date'].date()
            if 'dataset_size' in dbsDataset:
                sizeDataset = float(dbsDataset['dataset_size'])
            elif 'size' in dbsDataset:
                sizeDataset = float(dbsDataset['size'])
        else:
            ageDataset=None
            sizeDataset=None

        spDataset=dataset.split('/')
        # caching variables to avoid extensive loopups

        cacheES={}
        for cat in dataCategories:
            cacheES[cat] = phedexInfo[cat].get(dataset,None)

        #loop over the set of plots to make
        for key,valinfo in keyInfos.iteritems():
            #the plot has two attributes, the time period and the data sample
            ageKey = valinfo[0]#findAgeKey(key)
            dsKey=valinfo[1]#(spKey[0])
            #stop the loop if the dataset is not part of the plot
            if not interestingDataset(key,spDataset):
                continue

            #loopup the average size of the dataset for this time period
            for cat in dataCategories:#range(3):
                m=0
    #            if "All" in cacheES:
    #                if dsKey in cacheES["All"]:
    #                    m=cacheES["All"][dsKey]
    #right
                if cat in cacheES:
                    if dsKey in cacheES[cat]:
                        m=cacheES[cat][dsKey]

                nCopies=1.
                counter=0.

                #optionally compute the number of copies (on average) of the dataset on disk
                #by comparing its average size to the size in dbs
                #again only works if dataset is known to dbs
                if divideByNCopies and (sizeDataset is not None):
                    nCopies=m/sizeDataset

                #compute the average number of times each file in the dataset is accessed
                #using popularity data and copies on disk
                #divide but protect against case where the dataset is not on disk
                if nCopies>0.:
                    counter=(classadsInfo[dsKey].get(dataset,0))/nCopies
                else:
                    counter=(classadsInfo[dsKey].get(dataset,0)) #this ought to be 0

                if counter > 0 and counter < 1:
                    # any access to the dataset counts - so round up
                    counter = 1
                else:
                    # otherwise round to the nearest integer value
                    counter = round(counter)

                    #distinguish the 0 bin between old and new datasets based on the 
                    #age of the dataset
                    if counter == 0:
                        if (ageDataset is not None) and (ageDataset < ageKey):
                            counter = -1 # 0 old

                #cut off the plot at the desired value
                if counter > maxPop:
                    counter=maxPop

                #store the results
                countsBySizeDict[cat][key][counter] = countsBySizeDict[cat][key].get(counter,0.)+m

                #test and printous
                if dataset == testDS:
                    print "Pop counter for",key,cat,"is", counter

                if cat=="AllOps":
                    fDump.write('%5d %7.5f %15s %s \n' % (counter,m,key,dataset))

    fDump.close()

    #tally up all the information
    sumsDict = computeSums()

    #plot everything
    import plotter
    from inputs import runLabel

    figNum=0

    for cat in dataCategories:#range(3):
        figNum = \
            plotter.plotPopularity(sumsDict[cat], cbs_keys, popularitySource, cat+'_'+popularitySource, figNum, iformat)


def main():
    "Main function"
    # step1: load DBS Info
    print("### load dbs events info ...")
    dbsInfo = readDBSInfo()

    # step2: generate Phedex means
    print("### load phedex means ...")
    if not loadPhedexMeans:
        savePhedexMeans()
    phedexInfo = readPhedexMeans()

    # step3: generate ClassAds data or popularity
    if popularitySource.lower().startswith('popdb'):
        print("### load popdb ...")
        if not loadPopDB:
            savePopDB(dbsInfo)
        classadsInfo = readPopDB()
    else:
        print("### load classads ...")
        if not loadClassAds:
            saveClassAds(dbsInfo)
        classadsInfo = readClassAds()

    # step4: create plots
    print("### generate plots ...")
    plots(phedexInfo, dbsInfo, classadsInfo, iformat)

if __name__ == '__main__':
    main()
