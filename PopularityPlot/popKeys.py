#!/usr/bin/env python

# local modules
from inputs import loadOptions
# load options first since they define all inputs parameters
if __name__ == '__main__':
    loadOptions()
from inputs import intervals, dataTypes

#interested in these dataset combinations
#dataTypes= ['All','AOD','AODSIM','MINIAOD','MINIAODSIM',
#            'sAODs','Upgrade','RECO','GENSIMRECO',
#            'GENSIMRAW','RAW','ALCARECO','Other',
#            'GENSIM','GEN','LHE','USER',
#            'FEVT','PREMIXRAW','RAWAODSIM','DQMIO',
#            'GENSIMRECODEBUG','GENRAW','RAWRECO']
#dataTypes= ['All']

cbs_keys=[]
for d in dataTypes:
    for i in intervals:
        cbs_keys.append(i+" "+d)

#just to avoid endless splitting
spKeys={}
for key in cbs_keys:
    spKeys[key]=(key.split())

#the dataset and cbs_key information gets stored in these dictionaries
dataCategories=["All","AnaOps","AllOps"]
countsBySizeDict={}
for cat in dataCategories:
    countsBySizeDict[cat]=dict()
    for key in cbs_keys:
        countsBySizeDict[cat][key]=dict()
#countsBySize={}
#countsBySizeAnaOps={}
#countsBySizeAllOps={}

#for key in cbs_keys:
#    countsBySize[key]=dict()
#    countsBySizeAnaOps[key]=dict()
#    countsBySizeAllOps[key]=dict()

#countsBySizeArr=[countsBySize,countsBySizeAnaOps,countsBySizeAllOps]

#helper function to get the right starting key 
#this can certainly be done better
def findAgeKey(key):
    from utils import dStarts
    return dStarts[spKeys[key][0]]

#get the age in terms of number of days
#again, can be better..
def findNDaysKey(key):
    from utils import nDaysDict
    return nDaysDict[spKeys[key][0]]

# functions to define interesting or not interesting datasets
# need one function corresponding to each cbs_key
def isAll(spDataset):
    return True
def isAOD(spDataset):
    return  spDataset[-1]=="AOD"
def isAODSIM(spDataset):
    return  spDataset[-1]=="AODSIM"
def isMINIAOD(spDataset):
    return  spDataset[-1]=="MINIAOD"
def isMINIAODSIM(spDataset):
    return  spDataset[-1]=="MINIAODSIM"
def isRECO(spDataset):
    return  spDataset[-1]=="RECO"
def isGENSIMRECO(spDataset):
    return  spDataset[-1]=="GEN-SIM-RECO"
def isGENSIMRAW(spDataset):
    return  spDataset[-1]=="GEN-SIM-RAW"
def isRAW(spDataset):
    return  spDataset[-1]=="RAW"
def isALCARECO(spDataset):
    return  spDataset[-1]=="ALCARECO"
def issAODs(spDataset):
    return spDataset[-1] in ["AOD","AODSIM","MINIAOD","MINIAODSIM"]
def isUpgrade(spDataset):
    return ("upgrade2023" in spDataset[-2]) and (not issAODs(spDataset))
def isOther(spDataset):
    return not (issAODs(spDataset) or isUpgrade(spDataset))
def isGENSIM(spDataset):
    return spDataset[-1]=="GEN-SIM"
def isGEN(spDataset):
    return spDataset[-1]=="GEN"
def isLHE(spDataset):
    return spDataset[-1]=="LHE"
def isUSER(spDataset):
    return spDataset[-1]=="USER"
def isFEVT(spDataset):
    return spDataset[-1]=="FEVT"
def isPREMIXRAW(spDataset):
    return spDataset[-1]=="PREMIX-RAW"
def isRAWAODSIM(spDataset):
    return spDataset[-1]=="RAWAODSIM"
def isDQMIO(spDataset):
    return spDataset[-1]=="DQMIO"
def isGENSIMRECODEBUG(spDataset):
    return spDataset[-1]=="GEN-SIM-RECODEBUG"
def isGENRAW(spDataset):
    return spDataset[-1]=="GEN-RAW"
def isRAWRECO(spDataset):
    return spDataset[-1]=="RAW-RECO"


#using the functions above, call the one corresponding 
#to the key in use and apply it to the dataset
def interestingDataset(key,dataset):
    spKey=spKeys[key]
    method="is"+spKey[1]
    return globals()[method](dataset)

# after all the datasets and keys have been tallied up
# compute the sums to be plotted
def computeSums():
    from inputs import maxPop
    import numpy
    sumsDict={}
    for cat in dataCategories:
        sumsDict[cat]=[]

        for i in range(-1,maxPop+1):
            sum=numpy.zeros(len(cbs_keys)+1)
            for j,key in enumerate(cbs_keys):
                if i in countsBySizeDict[cat][key]:
                    sum[j+1]=sum[j+1]+countsBySizeDict[cat][key][i]/1024./1024./1024./1024./1024.
            sumsDict[cat].append(sum)
    return sumsDict
