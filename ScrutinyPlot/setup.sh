#!.bin/bash

# setup proper environment for run.sh script
# it should include python ROOT package, FWLite from CMSSW

# here is a setup for vocms092 (cmspopdb)
if [ "`hostname -s`" == "vocms092" ]; then
    export SCRAM_ARCH=slc7_amd64_gcc700
    export PATH=$PATH:/cvmfs/cms.cern.ch/common
    alias cmsenv='eval `scramv1 runtime -sh`'
    cd /data/cms/CMSSW/CMSSW_10_2_5
    eval `scramv1 runtime -sh`
    cd -
fi
