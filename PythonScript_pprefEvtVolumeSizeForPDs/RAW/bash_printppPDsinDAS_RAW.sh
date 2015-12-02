#!/bin/bash
cd /afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src
eval `scramv1 runtime -sh` 

#dt=`date '+%b%d_%Hh%Mm'`

python /afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src/PythonScript_pprefEvtVolumeSizeForPDs/RAW/printppPDsinDAS_RAW.py &> /afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src/PythonScript_pprefEvtVolumeSizeForPDs/RAW/output_printppPDsinDAS_RAW.txt
