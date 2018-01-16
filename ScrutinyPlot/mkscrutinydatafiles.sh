#!/bin/bash

# Required arguments
# $1 -- Name of Phedex CSV file with these fields
# site,dataset,rdate,gid,min_date,max_date,ave_size,max_size,days
# $2 -- Directory containing dataset*.csv files with these fields
# dataset,user,ExitCode,Type,TaskType,sum_evts,sum_chr,date,rate,tier

wkdir=/tmp/$USER/popularity
mkdir -p $wkdir

# 1. Get datasets and their sizes
# Fields 2, 7, and 6 are dataset name, average size, and end date of its presence
awk -F , '{print $2 "," $7 "," $6}' "$1" | grep -v 'dataset,ave' | sort -t , -k 1,1 -u >> $wkdir/dsandsz$$.txt

# 2. Get daily accesses for each dataset
for jobdtfile in "$2"/dataset*.csv ; do
	# Fields 1 and 8 are dataset name and access date
	grep -v 'dataset,user,ExitCode,' $jobdtfile | awk -F , '{print $1 "," $8}' | grep -v 'null,' | sort >> $wkdir/dsuses$$.txt
done

# 3. Add up uses/day for each DS
awk -F , -f sumDailyUses.awk $wkdir/dsuses$$.txt |  sort -t , -k1,1 > $wkdir/sumdsuses$$.txt
# sumdsuses$$.txt fields are dataset name, access date, and number of accesses for that date

# 4. Join uses and sizes
join -t , -j 1 $wkdir/dsandsz$$.txt $wkdir/sumdsuses$$.txt > $wkdir/sumusesz$$.txt
# sumusesz$$.txt fields are dataset name, size, dummy date, access date, and number of accesses for that date

# 5. Create two subset files by date
# Field 4 is the access date
awk -F , '{if ($4 > 20171108) {print $0}}' $wkdir/sumusesz$$.txt  > $wkdir/dayuses1month$$.txt
awk -F , '{if ($4 > 20170908) {print $0}}' $wkdir/sumusesz$$.txt  > $wkdir/dayuses3month$$.txt
# Uses files fields are dataset name, size, dummy date, access date, and number of accesses for that date

# 6. Sum up all daily uses for each dataset
awk -F , -f sumAllUses.awk $wkdir/sumusesz$$.txt > $wkdir/usesfullperiod$$.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses1month$$.txt > $wkdir/uses1month$$.txt
awk -F , -f sumAllUses.awk $wkdir/dayuses3month$$.txt > $wkdir/uses3months$$.txt
# Fields are dataset name, size, number of accesses for period


# 6. Get list of unused datasets
# 7. Get the total size of unused datasets
function getUnused {  # $1 is earliest date for dataset, $2 is uses file for period
	join -t , -j 1 -v 1 $wkdir/dsandsz$$.txt $2 > $wkdir/unusedDS$1$$.txt
	# unusedDS$$.txt fields are dataset name, size, date of last presence

	unusedtot=`awk -F , -v begindate=$1 '{ if ($3 > begindate) {sum = sum + $2}} END{print sum}' $wkdir/unusedDS$1$$.txt`
	echo Unused total `expr $unusedtot / 1024 / 1024 / 1024` GB

	# 8. Add entry for unused datasets to uses file
	echo "not_used,$unusedtot,0" >> $2
}

getUnused 20171108 $wkdir/uses1month$$.txt
getUnused 20170908 $wkdir/uses3months$$.txt
getUnused 20170615 $wkdir/usesfullperiod$$.txt
