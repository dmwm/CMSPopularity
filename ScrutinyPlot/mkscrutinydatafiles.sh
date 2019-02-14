#!/bin/bash

# Required arguments
# $1 -- Name of Phedex CSV file with these fields
# site,dataset,rdate,gid,min_date,max_date,ave_size,max_size,days
# $2 -- Name of DBS CSV files with these fields:
# dataset,size,nfiles,nevents # this format Carl used
# or
# dataset,creation_date,size,nfiles,nevents # this format is used by cms-plots
#
# $3 -- Directory containing jobUse*.csv files with these fields
# dataset,user,ExitCode,Type,TaskType,rec_time,sum_evts,sum_chr,date,rate,tier

# Set these values

# Beginning of date range
#begindtrng=20170101
begindtrng=20171001

# End of date range
#enddtrng=20180131
enddtrng=20181031

# Mid-point of date range (6-month point if full year range)
#middt=20170701
middt=20170301

# Last portion of date range (3 months to the end for full year range)
#lastfracdt=20171001
lastfracdt=20180901

wkdir=/tmp/$USER/popularity
mkdir -p $wkdir

if [ $# -ne 3 ] || [ "$1" == "-h" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]; then
    echo "Usage: mkscrutinydatafiles.sh <phedex csv> <dbs csv> <directory with jobUse*.csv files>"
		exit 0
fi

phedexcsv=$1
dbscsv=$2
jobsdir=$3

filename=$(basename "$phedexcsv")
phedexext="${filename##*.}"
filename=$(basename "$dbscsv")
dbsext="${filename##*.}"

# 1. Get datasets and their sizes, but only for T1 and T2 sites
# Fields 2, 7, 3, and 6 are dataset name, average size, replica date and end date of its presence
if [ "$phedexext" == "csv" ]; then
    awk -F , '$1 ~ /T1.*/ || $1 ~ /T2.*/ {if ($7 > 0) {print $2 "," $7 "," $3 "," $6}}' "$phedexcsv" | grep -v -e 'dataset,ave' -e RelVal | sort -t , -k 1,1 -k 3,3 -k 4,4 > $wkdir/dsandsz.txt
elif [ "$phedexext" == "gz" ]; then
    zcat $phedexcsv | awk -F , '$1 ~ /T1.*/ || $1 ~ /T2.*/ {if ($7 > 0) {print $2 "," $7 "," $3 "," $6}}' | grep -v -e 'dataset,ave' -e RelVal | sort -t , -k 1,1 -k 3,3 -k 4,4 > $wkdir/dsandsz.txt
else
    echo "Unsupported phedex file name: $phedexcsv"
    exit 1
fi
python calcDSSizes.py $wkdir/dsandsz.txt $lastfracdt $middt $begindtrng $enddtrng > $wkdir/dsSzLif.txt

# PLEASE NOTE: there are two types of dbs_events files
# if dbs events file is created with creation_date we need to use $5 (it has 5 fields)
# otherwise we need to use $4 (it has 4 fields)
if [ "$dbsext" == "csv" ]; then
    awk -F , '{print $1 "," $5}' "$dbscsv" | sed 's/"//g' | sort -t , -k1,1 > $wkdir/dsEvts.txt
elif [ "$dbsext" == "gz" ]; then
    zcat $dbscsv | awk -F , '{print $1 "," $5}' | sed 's/"//g' | sort -t , -k1,1 > $wkdir/dsEvts.txt
else
    echo "Unsupported dbs file name: $dbscsv"
    exit 1
fi
# dsEvts has dataset and number of events
join -t , -j 1 $wkdir/dsSzLif.txt $wkdir/dsEvts.txt > $wkdir/dsSzDur.txt
# dsSzDur has dataset, size3month, size6month, size12month, begin date, end date, and number of events

# 2. Get daily accesses for each dataset
for jobdtfile in "$jobsdir"/*.csv ; do
	# Fields 1 and 7 are dataset name and kilo events used. Access date is not reliable -- use file name
#    accdate=`echo $jobdtfile | sed 's/.*jobUse\(.*\)\..*/\1/'`
    # we require that jobdtfile name had a YYYYMMDD timestamp in its name, e.g.
    # dataset-YYYYMMDD.csv
    accdate=`basename $jobdtfile | awk '{split($0,a,"[.-]"); print a[2]}'`
	grep -v 'dataset,user,ExitCode,' $jobdtfile | awk -F , -v accdate=$accdate '{if ($7 != "null" && $7 > 0) {print $1 "," accdate "," $7 * 1000}}' | sed 's/"//g' | grep -v 'null' | sort -t , -k1,1 >> $wkdir/dsuses.txt
done

# 3. Add up uses/day for each DS
awk -F , -f sumDailyUses.awk $wkdir/dsuses.txt |  sort -t , -k1,1 -k2,2 > $wkdir/sumdsuses.txt
# sumdsuses.txt fields are dataset name, access date, and number of events used for that date

# 4. Join uses and sizes
join -t , -j 1 $wkdir/dsSzDur.txt $wkdir/sumdsuses.txt > $wkdir/sumusesz.txt
# sumusesz.txt fields are dataset name, size3month, size6month, size12month, begin date, end date, dataset events, access date, and number of events for that date

awk -F , '{if ($5 > 0) {print $1 "," $2 "," $3 "," $4 "," $9/$7 "," $8}}' $wkdir/sumusesz.txt > $wkdir/sumEvtsusesz.txt
# sumEvtsusesz.txt fields are dataset name, size3month, size6month, size12month, amount of ds read, access date

# 5. Create two subset files by date
# Field 4 is the access date
awk -F , -v dtboundary=$lastfracdt '{if ($6 >= dtboundary) {print $1 "," $2 "," $5 "," $6}}' $wkdir/sumEvtsusesz.txt  > $wkdir/dayuses3month.txt
awk -F , -v dtboundary=$middt '{if ($6 >= dtboundary) {print $1 "," $3 "," $5 "," $6}}' $wkdir/sumEvtsusesz.txt  > $wkdir/dayuses6month.txt
awk -F , '{print $1 "," $4 "," $5 "," $6}' $wkdir/sumEvtsusesz.txt  > $wkdir/dayuses12month.txt
# Uses files fields are dataset name, size, amount of ds read, access date

# 6. Sum up all daily uses for each dataset
awk -F , -f sumAllUses.awk $wkdir/dayuses12month.txt > $wkdir/usesfullperiod.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses6month.txt > $wkdir/uses6month.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses3month.txt > $wkdir/uses3months.txt
# Fields are dataset name, size, amount of ds read


# 6. Get list of unused datasets
# 7. Get the total size of unused datasets
function getUnused {  # $1 is earliest date for dataset, $2 is uses file for period, $3 is for the file position of the size
	join -t , -j 1 -v 1 $wkdir/dsSzDur.txt $2 > $wkdir/unusedDS$1.txt
	# unusedDS.txt fields are dataset name, size3month, size6month, size12month, begin date, end date of last presence, and number of events

	unusedtotnow=`awk -F , -v begindate=$1 -v enddate=$enddtrng -v sizepos=$3 '{ if ($5 >= begindate && $5 <= enddate) {sum = sum + $sizepos}} END{print sum}' $wkdir/unusedDS$1.txt`
	unusedtotold=`awk -F , -v begindate=$1  -v sizepos=$3 '{ if ($5 < begindate && $6 >= begindate) {sum = sum + $sizepos}} END{print sum}' $wkdir/unusedDS$1.txt`
	[ -z "$unusedtotnow" ] && unusedtotnow=0
	[ -z "$unusedtotold" ] && unusedtotold=0
	echo Unused total `expr $unusedtotnow / 1024 / 1024 / 1024` GB
	echo Unused total `expr $unusedtotold / 1024 / 1024 / 1024` GB

	# 8. Add entry for unused datasets to uses file
	echo "not_used,$unusedtotnow,0" >> $2
	echo "not_used,$unusedtotold,-1" >> $2
}

getUnused $lastfracdt $wkdir/uses3months.txt 2
getUnused $middt $wkdir/uses6month.txt 3
getUnused $begindtrng $wkdir/usesfullperiod.txt 4
