#!/usr/bin/env python
#
# modified Script to print information about the pp Reference Run PDs in DAS in table format
#
 
from datetime import datetime
import os
from prettytable import PrettyTable
from prettytable import ALL

Dir = "/afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src/PythonScript_pprefSiteInfo"
 
pdNames = ["HIMinimumBias1"]

pdNames.append("L1MinimumBias")
pdNames.append("EmptyBX")
pdNames.append("HighPtLowerJets")
pdNames.append("HighPtJet80")
pdNames.append("HighPtLowerPhotons")
pdNames.append("HighPtPhoton30AndZ")
pdNames.append("HIOniaTnP")
pdNames.append("HIEWQExo")
pdNames.append("HIOnia")
pdNames.append("FullTrack")
pdNames.append("HighMultiplicity")
pdNames.append("ppForward")
pdNames.append("HeavyFlavor")
pdNames.append("HIHardProbes")

pdNum = len(pdNames)
x = PrettyTable(["PD Names","Site, Dataset Presense"])
x.align = "c"
x.valign = "m"
x.hrules = ALL
x.padding_width = 1

for pdName in pdNames:
    dasAODPathName = '/' + pdName + '/Run2015E-PromptReco-v1/AOD'

    findSitesAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="site dataset=' + dasAODPathName + ' | grep site.name,site.dataset_fraction" > tmp.txt ; tail -n +4 tmp.txt > sites.txt'
    os.system(findSitesAODCommand)

    fileInput = open('sites.txt', 'r')
    SiteNames = []
    for line in fileInput:
        tmpname = line.rstrip('\n')
        SiteNames.append(tmpname)

    for SiteName in SiteNames:
        if SiteName.find('Buffer') > 0:
            SiteNames.remove(SiteName)
        if SiteName.find('MSS') > 0 :
            SiteNames.remove(SiteName)
         
    SiteForThisPD = '\n'.join(SiteNames)

#    print SiteForThisPD 
    
    fileInput.close()
 
    x.add_row([pdName,SiteForThisPD])
print x

exit()
