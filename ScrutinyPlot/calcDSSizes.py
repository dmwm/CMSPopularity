# Calculate the weighted average size of datasets across CMS sites, taking into account the number of replicas
# $1 -- file name with dataset info
# $2 -- Start date of 3-month period
# $3 -- Start date of 6-month period
# $4 -- Start date of 12-month period
# $5 -- End date of period

import datetime
import sys

def calcDaySz(avgsz, beginDate, lastDate, startDate, endDate, dsHistory):
 if (beginDate < startDate) :
  beginDate = startDate
 if (lastDate > endDate) :
  lastDate = endDate
 beginDateStr = str(beginDate)
 lastDateStr = str(lastDate)
 beginDt = datetime.date(int(beginDateStr[0:4]), int(beginDateStr[4:6]), int(beginDateStr[6:8]))
 lastDt = datetime.date(int(lastDateStr[0:4]), int(lastDateStr[4:6]), int(lastDateStr[6:8]))
 if lastDt >= beginDt :
  # daysSz = avgsz * ((lastDt - beginDt).days + 1)
  siteLife = ((lastDt - beginDt).days + 1)
  # print "daysz", ds, beginDt, lastDt, avgsz, daysSz
 else :
  siteLife = 0
 siteStat = [ avgsz, siteLife ]
 dsHistory.append(siteStat)
 return dsHistory

def calcCMSSz(startDate, endDate, endLife, dsHistory) :
 cmsSz = 0
 if endLife >= startDate and endDate >= startDate :
  startDateStr = str(startDate)
  endDateStr = str(endDate)
  startDttm = datetime.date(int(startDateStr[0:4]), int(startDateStr[4:6]), int(startDateStr[6:8]))
  endDttm = datetime.date(int(endDateStr[0:4]), int(endDateStr[4:6]), int(endDateStr[6:8]))
  periodDur = ((endDttm - startDttm).days + 1)
  for siteLife in dsHistory :
   cmsSz += siteLife[0] * (float(siteLife[1]) / float(periodDur))
 return cmsSz

def calcAndPrint(startDate3mon, startDate6mon, startDate12mon, endDate, endLife, dsHist3mon, dsHist6mon, dsHist12mon) :
 cmsSz3mon = calcCMSSz(startDate3mon, endDate, endLife, dsHist3mon)
 cmsSz6mon = calcCMSSz(startDate6mon, endDate, endLife, dsHist6mon)
 cmsSz12mon = calcCMSSz(startDate12mon, endDate, endLife, dsHist12mon)
 print prevds + ",%d,%d,%d,%d,%d" % (int(cmsSz3mon), int(cmsSz6mon), int(cmsSz12mon), beginLife, endLife)


startDate3mon = int(sys.argv[2])
startDate6mon = int(sys.argv[3])
startDate12mon = int(sys.argv[4])
endDate = int(sys.argv[5])
beginLife = 21190101
endLife = 20100101
prevds = "start"
dsHist3mon = []
dsHist6mon = []
dsHist12mon = []

with open(sys.argv[1], "r") as infile :
 for inline in infile :
  entries = inline.split(",")
  ds = entries[0]
  if ds != prevds and prevds != "start" :
   calcAndPrint(startDate3mon, startDate6mon, startDate12mon, endDate, endLife, dsHist3mon, dsHist6mon, dsHist12mon)
   beginLife = 21190101
   endLife = 20100101
   dsHist3mon = []
   dsHist6mon = []
   dsHist12mon = []
  prevds = ds
  avgsz = int(entries[1])
  beginDate = int(entries[2])
  lastDate = int(entries[3])
  dsHist3mon = calcDaySz(avgsz, beginDate, lastDate, startDate3mon, endDate, dsHist3mon)
  dsHist6mon = calcDaySz(avgsz, beginDate, lastDate, startDate6mon, endDate, dsHist6mon)
  dsHist12mon = calcDaySz(avgsz, beginDate, lastDate, startDate12mon, endDate, dsHist12mon)
  if beginLife > beginDate :
    beginLife = beginDate
  if endLife < lastDate :
    endLife = lastDate

calcAndPrint(startDate3mon, startDate6mon, startDate12mon, endDate, endLife, dsHist3mon, dsHist6mon, dsHist12mon)
