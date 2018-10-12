# Basic documentation for popularity plotting scripts

This is a fork of David Lange cms-plots package:
Authors:
- David Lange code from gitlab.cern.ch/dlange/cms-plots which
- Valentin Kuznetsov code from gitlab.cern.ch/valya/cms-plots which

All setup is meant to be controled in input.py

**Input data sets needed**
1. Phedex data dumps (with at least site,dataset,rdate,gid,min_date,max_date,ave_size,max_size,days) - Format expected is unzipped CSV (files provided by Valentin are used as is after unzipping)
2. DBS data dumps (with at least dataset,date,num_file,num_event,file_size)- Format expected is unzipped CSV - code changes needed to interpret other csv layouts
3. Popularity data dumps (source dependent format)- classad format is a directory full of csv.gz files from Valentin

Currently the phedex dumps are taken from Valentin's work, the DBS dumps are done by a hacky script of mine, 
and the popularity data dumps are either from PopDB (crab only) or Valentin's classad dumps

**Running**

A simpliest way to run the machinery is to adjust run.sh script and run it.

Otherwise please follow this procedure (it is what run.sh does anyhow):
1. Edit input.py to be set up as desired (time intervals, popularity source, directory structure) 
2. Some preprocessing is needed. Run:
    1. python phedexMeans.py (this reads the phedex dumps and makes dumps of size on disk per day per dataset)
    2. python classadInput.py (if using the classad popularity)
3. python popularity

**The output should consist of** 
1. Some script printout of the plots (numpy arrays...)
2. pngs in outputdir/plots
3. csvs in outputdir/outCSV

the set of popularity plots (data tiers, subscription group, etc) to make is currently hardwired,
but quite a few are there.
 
