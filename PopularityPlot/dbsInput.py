#!/usr/bin/env python
import datetime
from inputs import dbsInput,dbsFormat
from utils import fopen

def readDBSInfo():
    dbsInfo={}

    print("### use dbsInput %s" % dbsInput)
    with fopen(dbsInput) as istream:
        headers = None
        while True:
            line = istream.readline().replace('\n', '')
            if not line:
                break
            row = line.split(',')
            if not headers:
                headers = row
                continue
            rdict = dict(zip(headers, row))
            dataset = rdict.pop('dataset').replace('"', '')
            for key in rdict.keys():
                rdict[key] = float(rdict[key])
            if 'date' in headers:
                rdict['creation_date'] = datetime.datetime.fromtimestamp(rdict['date'])
            elif 'creation_date' in headers:
                rdict['creation_date'] = datetime.datetime.fromtimestamp(rdict['creation_date'])
            dbsInfo[dataset] = rdict
    return dbsInfo
