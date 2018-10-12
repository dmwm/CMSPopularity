#!/usr/bin/env python

# system modules
import sys
import datetime

# third party modules
import numpy
# a dump of all known phedex GIDs
#{"phedex":{"request_timestamp":1513095921.57439,"instance":"prod","request_url":"http://cmsweb.cern.ch:7001/phedex/datasvc/json/prod/groups","request_version":"2.4.0pre1","group":[{"name":"AnalysisOps","id":"42"},{"name":"B2G","id":"163"},{"name":"DataOps","id":"18"},{"name":"FacOps","id":"19"},{"name":"IB RelVal","id":"106"},{"name":"RelVal","id":"107"},{"name":"SMP","id":"162"},{"name":"b-physics","id":"8"},{"name":"b-tagging","id":"5"},{"name":"caf-alca","id":"102"},{"name":"caf-comm","id":"103"},{"name":"caf-lumi","id":"164"},{"name":"caf-phys","id":"104"},{"name":"deprecated-ewk","id":"2"},{"name":"deprecated-qcd","id":"16"},{"name":"deprecated-undefined","id":"142"},{"name":"dqm","id":"122"},{"name":"e-gamma_ecal","id":"4"},{"name":"exotica","id":"15"},{"name":"express","id":"108"},{"name":"forward","id":"17"},{"name":"heavy-ions","id":"10"},{"name":"higgs","id":"6"},{"name":"jets-met_hcal","id":"9"},{"name":"local","id":"22"},{"name":"muon","id":"3"},{"name":"susy","id":"12"},{"name":"tau-pflow","id":"13"},{"name":"top","id":"7"},{"name":"tracker-dpg","id":"14"},{"name":"tracker-pog","id":"82"},{"name":"trigger","id":"11"},{"name":"upgrade","id":"105"}],"request_call":"groups","call_time":0.00231,"request_date":"2017-12-12 16:25:21 UTC"}}

# local modules
from inputs import isTest, testDS, phedexDataFile
from utils import dStartOldest, dEnd, nDays, getDate, fopen, object_size

def isAll(keyInfo):
    return True
def isAnaOps(keyInfo):
    if keyInfo[2]=="42": return True
    return False
def isAllOps(keyInfo):
    if keyInfo[2]=="42": return True
    if keyInfo[2]=="18": return True
    if keyInfo[2]=="19": return True
    return False
def isMinusOne(keyInfo):
    if keyInfo[2]=="-1": return True
    return False

def readSizes():
    #replica level information
    phedexInfo={}
    #dataset level information
    phedexDatasetInfo={}

    #site,dataset,rdate,gid,min_date,max_date,ave_size,max_size,days
    colsPhedex={ "site" :-1,
                 "dataset" : -1,
                 "rdate" : -1,
                 "min_date" : -1,
                 "max_date" : -1,
                 "ave_size" : -1,
                 "max_size" : -1,
                 "days" : -1,
                 "gid" : -1
    }

    colPhedexNames=colsPhedex.keys()

    nCount=0
    print("### use phedexDataFile %s" % phedexDataFile)
    print("### testDS %s" % testDS)
    istream = fopen(phedexDataFile)
    for l in istream:
        nCount=nCount+1
        #optionaly test things on a subset of data
        if isTest and nCount > 10000: 
            print "Incomplete data as you are just testing"
            break
        sp=l.strip().split(',')
        #use the first row to understand the set of columns
        #stop if the data is not in the expected format
        if nCount==1:
            for col in colPhedexNames:
                for i in range(0,len(sp)):
                    if col == sp[i] : colsPhedex[col]=i
                if colsPhedex[col]==-1:
                    print "missing column",col
                    print("File: %s" % phedexDataFile)
                    sys.exit(1)
#            print("### colsPhedex", colsPhedex)
        else:
            #create the dictionaries from the phedex csvs
            dataset=sp[colsPhedex["dataset"]]
            site=sp[colsPhedex["site"]]
            rdate=sp[colsPhedex["rdate"]]
            gid=sp[colsPhedex["gid"]]
            #skip anything that is relval
            if 'RelVal' in dataset: continue
            key = (dataset,site,rdate,gid)
            #should become try: blah except: blah 
            if dataset not in phedexDatasetInfo:
                phedexDatasetInfo[dataset]=[]
            #this can then be used to look up detailed information in phedexInfo dictionary
            phedexDatasetInfo[dataset].append((site,rdate,gid))

            datum={}
            for col in colPhedexNames:
                if col == "site": continue
                if col == "dataset": continue
                datum[col]=sp[colsPhedex[col]]
            #catch errors - there should never be a repeated key
            if key in phedexInfo:
                print "Duplicated key"
                print key
                print sp
                print phedexInfo[key]
                sys.exit(1)
            #done, just store everything..
            phedexInfo[key]=datum
            if testDS in key:
                print("### testDS", key, datum)

    istream.close()
                
    replicas=phedexInfo.keys()
    nRep=len(replicas)

    #now make dataset level arrays that contain day-by-day size on T1/T2 disk
    #do that for analysis ops and comp ops and gid=-1 (which is a nonsense value)
    esDictKeys=["All","AnaOps","AllOps","MinusOne"]
    effectiveSizesDict={}
    effectiveSizesFunc={}
    for key in esDictKeys:
        effectiveSizesDict[key]={}
        method="is"+key
        effectiveSizesFunc[key]= globals()[method]

    print("phedexDatasetInfo", len(phedexDatasetInfo.keys()), "size", object_size(phedexDatasetInfo))

    #loop over dataset and replicas
    for dataset,keyInfos in phedexDatasetInfo.iteritems():
        #again, skip relvals here - even if there should be none
        if "/RelVal" in dataset: 
            continue
        #create the arrays
        cacheES={k : numpy.zeros(nDays) for k in esDictKeys}
        for key,val in cacheES.iteritems():
            effectiveSizesDict[key][dataset]=val

        #get the list replicas for this dataset
        #keyInfos=phedexDatasetInfo[dataset]
        #loop over them
        for keyInfo in keyInfos:
            site=keyInfo[0]
            #skip things that are not T1 or T2
            if 'T1' not in site and 'T2' not in site:
                continue #no T3 no T0

            #get the detailed phedex information for this replica
            phKey=(dataset,)+keyInfo
            phDatum=phedexInfo[phKey]
            d1=getDate(phDatum["min_date"])
            d2=getDate(phDatum["max_date"])

            #compute the range of days that this replica was on disk
            indEnd = (d2-dStartOldest).days if d2 <dEnd else nDays -1
            if indEnd<0:
                continue #sample was gone before the period we are looking at
            indStart = (d1-dStartOldest).days if d1>dStartOldest else 0

            #just some printouts for debugging if you want them
            if dataset == testDS:
                print site,phKey,phDatum
                print d1,d2
                print "start and end",indStart,indEnd
                print float(phDatum['ave_size'])

            #set the daily size to the average seen in the phedex dumps
            for key,val in effectiveSizesFunc.iteritems():
                if val(keyInfo):
                    cacheES[key][indStart:indEnd+1]+=float(phDatum['ave_size'])
    return effectiveSizesDict

if __name__ == "__main__":


    #some basically obsolete stuff
    import datetime

    nLTDate=0
#    nGTDate=0
#    for rep in replicas:
#        datum=phedexInfo[rep]
#    #    print datum["min_date"]
#        d1=getDate(datum["min_date"])
#        d2=getDate(datum["max_date"])
#        days=(d2-d1).days+2 #inclusive ranges
#        if days > datum["days"]:
#            nGTDate=nGTDate+1
#        if days < datum["days"]:
#            nLTDate=nLTDate+1
##    print d1,d2,days,datum["days"],datum["min_rdate"],datum["max_rdate"],rep
#    print "Check on dates", nRep,nLTDate,nGTDate
#
#    f=open('allDatasets2.out','w')
#    for k in phedexDatasetInfo:
#        f.write(k+'\n')
#    f.close()
