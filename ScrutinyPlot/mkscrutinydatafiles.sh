#!/bin/bash

# Required arguments
# $1 -- Name of Phedex CSV file with these fields
# site,dataset,rdate,gid,min_date,max_date,ave_size,max_size,days
# $2 -- Name of DBS CSV files with these fields:
# dataset,size,nfiles,nevents
# $3 -- Directory containing dataset*.csv files with these fields
# dataset,user,ExitCode,Type,TaskType,sum_evts,sum_chr,date,rate,tier

wkdir=/tmp/$USER/popularity
mkdir -p $wkdir

# 1. Get datasets and their sizes
# Fields 2, 7, 5, and 6 are dataset name, average size, begin and end date of its presence
awk -F , '{print $2 "," $7 "," $5 "," $6}' "$1" | grep -v 'dataset,ave' | sort -t , -k 1,1 -k 4,4 -k 5,5 > $wkdir/dsandsz$$.txt
awk -F , -f findDSlifetime.awk $wkdir/dsandsz$$.txt > $wkdir/dsSzLif$$.txt
awk -F , '{print $1 "," $4}' $2 | sort -t , -k1,1 > $wkdir/dsEvts$$.txt
# dsEvts has dataset and number of events
join -t , -j 1 $wkdir/dsSzLif$$.txt $wkdir/dsEvts$$.txt > $wkdir/dsSzDur$$.txt
# dsSzDur has dataset, size, begin date, end date, and number of events

# 2. Get daily accesses for each dataset
for jobdtfile in "$3"/dataset*.csv ; do
	# Fields 1, 8, and 6 are dataset name, access date, and kilo events used
	grep -v 'dataset,user,ExitCode,' $jobdtfile | awk -F , '{if ($6 != "null" && $6 > 0) {print $1 "," $8 "," $6 * 1000}}' | grep -v 'null,' | sort >> $wkdir/dsuses$$.txt
done

# 3. Add up uses/day for each DS
awk -F , -f sumDailyUses.awk $wkdir/dsuses$$.txt |  sort -t , -k1,1 > $wkdir/sumdsuses$$.txt
# sumdsuses$$.txt fields are dataset name, access date, number of accesses, and number of events used for that date

# 4. Join uses and sizes
join -t , -j 1 $wkdir/dsSzDur$$.txt $wkdir/sumdsuses$$.txt > $wkdir/sumusesz$$.txt
# sumusesz$$.txt fields are dataset name, size, begin date, end date, dataset events, access date, number of accesses, and number of events for that date

awk -F , '{if ($5 > 0) {print $1 "," $7 "," $2 * $8/$5 "," $6}}' $wkdir/sumusesz$$.txt > $wkdir/sumEvtsusesz$$.txt
# sumEvtsusesz$$.txt fields are dataset name, number of accesses, number of bytes read, access date

# 5. Create two subset files by date
# Field 4 is the access date
awk -F , '{if ($4 > 20171108) {print $0}}' $wkdir/sumEvtsusesz$$.txt  > $wkdir/dayuses1month$$.txt
awk -F , '{if ($4 > 20170908) {print $0}}' $wkdir/sumEvtsusesz$$.txt  > $wkdir/dayuses3month$$.txt
# Uses files fields are dataset name, number of accesses, number of bytes read, access date

# 6. Sum up all daily uses for each dataset
awk -F , -f sumAllUses.awk $wkdir/sumEvtsusesz$$.txt > $wkdir/usesfullperiod$$.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses1month$$.txt > $wkdir/uses1month$$.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses3month$$.txt > $wkdir/uses3months$$.txt
# Fields are dataset name, number of accesses for period, number of bytes for period


# 6. Get list of unused datasets
# 7. Get the total size of unused datasets
function getUnused {  # $1 is earliest date for dataset, $2 is uses file for period
	join -t , -j 1 -v 1 $wkdir/dsSzDur$$.txt $2 > $wkdir/unusedDS$1$$.txt
	# unusedDS$$.txt fields are dataset name, size, begin date, end date of last presence

	unusedtotnow=`awk -F , -v begindate=$1 '{ if (begindate <= $3) {sum = sum + $2}} END{print sum}' $wkdir/unusedDS$1$$.txt`
	unusedtotold=`awk -F , -v begindate=$1 '{ if (begindate > $3 && begindate <= $4) {sum = sum + $2}} END{print sum}' $wkdir/unusedDS$1$$.txt`
	echo Unused total `expr $unusedtotnow / 1024 / 1024 / 1024` GB
	echo Unused total `expr $unusedtotold / 1024 / 1024 / 1024` GB

	# 8. Add entry for unused datasets to uses file
	echo "not_used,0,$unusedtotnow" >> $2
	echo "not_used,-1,$unusedtotold" >> $2
}

getUnused 20171108 $wkdir/uses1month$$.txt
getUnused 20170908 $wkdir/uses3months$$.txt
getUnused 20170615 $wkdir/usesfullperiod$$.txt
