#!/bin/bash

datadir=/afs/cern.ch/work/c/cvuosalo/popularity/
wkdir=/tmp/cvuosalo/popularity
# 1. Get datasets and their sizes
# Fields 2, 7, and 6 are dataset name, average size, and end date of its presence
awk -F , '{print $2 "," $7 "," $6}' $datadir/ecomjobdata/phedex.csv | grep -v 'dataset,ave' | sort -t , -k 1,1 -u >> $wkdir/dsandsz$$.txt
# 2. Get daily accesses for each dataset
for jobdtfile in $datadir/ecomjobdata/dataset-201*.csv ; do
	# Fields 1 and 8 are dataset name and access date
	grep -v 'dataset,user,ExitCode,' $jobdtfile | awk -F , '{print $1 "," $8}' | grep -v 'null,' | sort >> $wkdir/dsuses$$.txt
done
# 3. Add up uses/day for each DS
awk -F , -f addup_uses.awk $wkdir/dsuses$$.txt |  sort -t , -k1,1 >> $wkdir/sumdsuses$$.txt
# 4. Join uses and sizes
join -t , -j 1 $wkdir/dsandsz$$.txt $wkdir/sumdsuses$$.txt >> $wkdir/sumusesz$$.txt
# 5. Create two subset files by date
# Field 4 is the access date
awk -F , '{if ($4 > 20171108) {print $0}}' $wkdir/sumusesz$$.txt  >> $wkdir/uses1month$$.txt
awk -F , '{if ($4 > 20170908) {print $0}}' $wkdir/sumusesz$$.txt  >> $wkdir/uses3month$$.txt
# 6. Get list of unused datasets
join -t , -j 1 -v 1 $wkdir/dsandsz$$.txt $wkdir/sumdsuses$$.txt >> $wkdir/unusedDS$$.txt
# 7. Get the total size of unused datasets
unusedtot=`awk -F , '{ if ($3 > 20170615) {sum = sum + $2}} END{print sum}' $wkdir/unusedDS$$.txt`
echo Unused total `expr $unusedtot / 1024 / 1024 / 1024` GB
# 8. Add entry for unused datasets to uses file
echo "not_used,$unusedtot,20170616,20170616,0" >> $wkdir/sumusesz$$.txt
