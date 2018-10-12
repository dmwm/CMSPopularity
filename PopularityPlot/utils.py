#!/usr/bin/env python

# system modules
import sys
import bz2
import gzip
import datetime

# local modules
from inputs import intervalEndString,intervalStartStrings,intervals

dStarts={}
nDaysDict={}
nDays=0
dEnd=datetime.datetime.strptime(intervalEndString,"%Y%m%d").date()
dStartOldest=dEnd #store the longest interval                                                                                         

for i in intervals:
    dStarts[i]=datetime.datetime.strptime(intervalStartStrings[i],"%Y%m%d").date()
    nDaysDict[i]=(dEnd-dStarts[i]).days+1
    if dStartOldest > dStarts[i]:
        dStartOldest=dStarts[i]
    if nDaysDict[i]>nDays:
        nDays=nDaysDict[i]

def object_size(data):
    "Return size of the data"
    if hasattr(data, 'tobytes'):
        return sys.getsizeof(data.tobytes())
    return sys.getsizeof(data)

def fopen(fin, mode='r'):
    "Return file descriptor for given file"
    if  fin.endswith('.gz'):
        stream = gzip.open(fin, mode)
    elif  fin.endswith('.bz2'):
        stream = bz2.BZ2File(fin, mode)
    else:
        stream = open(fin, mode)
    return stream

# retreive the data from a string - much faster that using dateutils directly                                                         
def getDate(d):
    import datetime
    return datetime.date(int(d[0:4]),int(d[4:6]),int(d[6:8]))
# the popularity dates from popDB have -s                                                                                             
def getDatePop(d):
    import datetime
    return datetime.date(int(d[0:4]),int(d[5:7]),int(d[8:10]))

