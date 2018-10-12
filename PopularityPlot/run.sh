#!/bin/bash

odir=$PWD/output
# cmspopdb nod settings
phedexInput=/data/cms/pop-data/phedex.csv.gz
dbsInput=/data/cms/pop-data/dbs_events.csv.gz
baseDir=/data/cms/pop-data/dbs_condor
classAdsInput=$baseDir
intervalDates="20171001,20170701,20170101"
intervalEnd=20180131

date=`date +%Y%m%d`
start_time="$(date -u +%s)"

echo "Job run on date : $date (`date`)"
echo "Phedex     input: $phedexInput"
echo "DBS        input: $dbsInput"
echo "ClassAds   input: $classAdsInput"
echo "Output area     : $odir"
echo "interval dates  : $intervalDates"
echo "interval ends   : $intervalEnd"
#echo "Title           : $title"

# step 1: generate phedex means
echo "Step 1: Run phedexMeans.py module"
python phedexMeans.py --output=$odir --phedexInput=$phedexInput --dbsInput=$dbsInput --baseDir=$baseDir --classAdsInput=$classAdsInput --intervalDates=$intervalDates --intervalEnd=$intervalEnd

# step 2: generate classAds
echo "Step 2: Run classadInput.py module"
python classadInput.py --output=$odir --phedexInput=$phedexInput --dbsInput=$dbsInput --baseDir=$baseDir --classAdsInput=$classAdsInput --intervalDates=$intervalDates --intervalEnd=$intervalEnd

# step 3: make plots
echo "Step 3: Run popularity.py module"
python popularity.py --output=$odir --phedexInput=$phedexInput --dbsInput=$dbsInput --baseDir=$baseDir --classAdsInput=$classAdsInput --intervalDates=$intervalDates --intervalEnd=$intervalEnd --loadClassAds --loadPhedexMeans

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
