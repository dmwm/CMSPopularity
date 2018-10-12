#!/bin/bash
# setup local environment
if [ -f $PWD/setup.sh ]; then
    source setup.sh
fi

# command to use
cmd=$PWD/mkscrutinydatafiles.sh

# location of our data
baseDir=/data/cms/pop-data

# location of phedex input dataframe, can be either in csv or csv.gz data-format
phedexInput=$baseDir/phedex.csv.gz

# location of dbs events input dataframe, can be either in csv or csv.gz data-format
dbsInput=$baseDir/dbs_events.csv.gz

# location of dbs_condor datasets, underlying files may be either in csv or csv.gz data-format
dbsCondorInput=$baseDir/dbs_condor

# title to apply to out plots
title="T1/T2 Dataset Usage for 2017-2018"

# generate image with format, supported png or pdf
iformat=pdf

# DO NOT EDIT BELOW THIS LINE

#odir=/tmp/valya/popularity
odir=`grep ^wkdir mkscrutinydatafiles.sh | awk '{split($1,a,"="); print a[2]}' | sed -s "s,\\$USER,$USER,g"`
rm -rf $odir
intervals=`egrep "^begindtrng|^enddtrng|^middt|^lastfracdt" $cmd | awk '{split($1,a,"="); print a[2]}' | sort | awk '{ORS=" "; print $0}'`
date=`date +%Y%m%d`
start_time="$(date -u +%s)"

echo "Job run on date : $date (`date`)"
echo "Phedex     input: $phedexInput"
echo "DBS        input: $dbsInput"
echo "DBS-Condor input: $dbsCondorInput"
echo "Output area     : $odir"
echo "intervals       : $intervals"
echo "Title           : $title"

$cmd $phedexInput $dbsInput $dbsCondorInput
python plot3periods.py $odir/usesfullperiod.txt $odir/uses6month.txt $odir/uses3months.txt $iformat "$title"

end_time="$(date -u +%s)"

elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
