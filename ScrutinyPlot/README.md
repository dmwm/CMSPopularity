These scripts create a scrutiny plot from DBS, Phedex, and job monitoring data.

An example of such data can be found here:

/afs/cern.ch/work/c/cvuosalo/popularity/dataFromCron

A sample command line is:

./mkscrutinydatafiles.sh ../dataFromCron/phedex_20170625_20180624.csv ../dataFromCron/dbsDSnumevts20180309.csv ../dataFromCron

That command produces three "uses" files, which you feed to the plotter to
get the scrutiny plot. The plotter requires any version of ROOT from the last few years.
A simple way to get ROOT into your path is to do cmsenv in a CMSSW release.

  $1 -- directory with uses files
python plot3periods.py $1/usesfullperiod*.txt $1/uses6month*.txt
$1/uses3months*.txt "T1/T2 Dataset Usage for June 25, 2017 to June 20, 2018"

