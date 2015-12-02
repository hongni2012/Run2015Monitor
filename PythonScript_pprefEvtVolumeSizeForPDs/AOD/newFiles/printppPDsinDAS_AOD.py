#!/usr/bin/env pytho/
#
# Script to print information about the AOD pp Reference Run PDs in DAS in table format
# Composed by Hong Ni and Charles Maguire
#
 
from datetime import datetime
import os
from prettytable import PrettyTable
from prettytable import ALL
import locale      # for printing location specific delimiters for large integers
locale.setlocale(locale.LC_ALL, 'en_US')

#Dir = "/afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src/PythonScript_pprefEvtVolumeSizeForPDs/AOD"
#Dir = "/gpfs21/scratch/maguire/CMSSW_7_5_5_patch3/src/Run2015Monitoring/MyProject/PythonScript_pprefEvtVolumeSizeForPDs/AOD/"
Dir = "."

breakDebug = False  # will process only the first PD
break2Debug = False  # will process only the first and second PDs
printDebug = False

fileOut = open("forCSV_output_printppPDsinDAS_AOD.txt", "w")

pdNames = ["MinimumBias1"]
pdNames.append("MinimumBias16")
pdNames.append("ppForward")
pdNames.append("HighMultiplicity")
pdNames.append("FullTrack")
pdNames.append("BTagCSV")
pdNames.append("HeavyFlavor")
pdNames.append("HighPtPhoton30AndZ")
pdNames.append("HighPtLowerPhotons")
pdNames.append("JetHT")
pdNames.append("HighPtJet80")
pdNames.append("HighPtLowerJets")
pdNames.append("DoubleMu")
pdNames.append("MuPlusX")
pdNames.append("SingleMuHighPt")
pdNames.append("SingleMuLowPt")

pdNum = len(pdNames)
x = PrettyTable(["PD Name","File Vol. (GB)","Max Lumi (GB)","Events (K)","Lumis","Evt Size (MB/Evt)","Lumi Size (GB/LS)"])
x.align["PD Name"] = "l"
x.padding_width = 1
x.float_format = .3;
x.hrules = ALL
forCSVx = PrettyTable(["PD Name","File Vol. (GB)","Max Lumi (GB)","Events (K)","Lumis","Evt Size (MB/Evt)","Lumi Size (GB/LS)"])
forCSVx.align["PD Name"] = "l"
forCSVx.padding_width = 1
forCSVx.float_format = .3;
forCSVx.hrules = ALL

now = datetime.now()
mm = str(now.month)
dd = str(now.day)
yyyy = str(now.year)
hour = str(now.hour)
mi = str(now.minute)
ss = str(now.second)
 
totalAODSize = 0
totalAODEvents = 0
totalLumis = 0
MaxFileSize = 0

countPDs = 0
for pdName in pdNames:
    countPDs += 1
    #if(pdName != 'HighPtPhoton30AndZ' and pdName != 'HighPtLowerPhotons'):
    #    continue
    print "Processing AOD dataset PD", pdName
    dasAODPathName = '/' + pdName + '/Run2015E-PromptReco-v1/AOD'
    findEventsAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="dataset dataset=' + dasAODPathName + ' | grep dataset.nevents" > tmp.txt ; tail -1 tmp.txt > events.txt'
    if(printDebug): print "findEventsAODCommand: ", findEventsAODCommand
    os.system(findEventsAODCommand)
    fileInput = open('events.txt', 'r')
    thisEvents = 0
    AODEventSize = 0
    nEventsK = 0
    for line in fileInput:
        nEvents = line.rstrip('\n')
        if(nEvents != '[]'):
            nEventsK = int(nEvents)/1.0e3 
            thisEvents = int(nEvents)
        else:
            nEvents = 0
            nEventsK = 0
        totalAODEvents += thisEvents
    fileInput.close()
 
    findSizeAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="dataset dataset=' + dasAODPathName + ' | grep dataset.size" > tmp.txt ; tail -1 tmp.txt > size.txt'
    if(printDebug): print "findSizeAODCommand: ", findSizeAODCommand
    os.system(findSizeAODCommand)
    fileInput = open('size.txt', 'r')
    AODFileSizeGB = 0
    for line in fileInput:
        AODFileSize = line.rstrip('\n')
        if(AODFileSize == '[]'):
            AODFileSizeGB = 0
        else:
            AODFileSizeGB = int(AODFileSize)/1.0e9
            if(thisEvents > 0):
               AODEventSize = AODFileSizeGB*1.0e3/thisEvents
        totalAODSize += AODFileSizeGB
    fileInput.close()

    countLumiAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="run,lumi dataset=' + dasAODPathName + ' | count(lumi)" > tmp.txt ; tail -1 tmp.txt > lumicounts.txt'
    if(printDebug): print "countLumiAODCommand: ", countLumiAODCommand
    os.system(countLumiAODCommand)
    fileInput = open('lumicounts.txt','r')
    thisLumis = 0
    for line in fileInput:
        nLumis = line.rstrip('\n')
        thisLumis = int(nLumis.strip('count(lumi)=')) 
        totalLumis += thisLumis

    if(thisLumis == 0):
        FileSizePerLumi = 0
    else:
        FileSizePerLumi = AODFileSizeGB/thisLumis
    fileInput.close()

    findMaxFileAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="file dataset=' + dasAODPathName + ' | max(file.size)" > tmp.txt ; tail -1 tmp.txt > maxfilesize.txt'
    if(printDebug): print "findMaxFileAODCommand: ", findMaxFileAODCommand
    os.system(findMaxFileAODCommand)
    fileInput = open('maxfilesize.txt','r')
    thisMaxSize = 0
    for line in fileInput:
        maxsize = line.strip('max(file.size)=')
        if(maxsize != '[]'):    
            thisMaxSize = int(maxsize)/1.0e9
    fileInput.close()
   
    aAODFileSizeGB = locale.format("%d", int(AODFileSizeGB), grouping=True)
    aEventsK = locale.format("%d", int(nEventsK), grouping=True)
    aLumis = locale.format("%d", thisLumis, grouping=True)
    x.add_row([pdName,aAODFileSizeGB,thisMaxSize,aEventsK,aLumis,AODEventSize,FileSizePerLumi])
    forCSVx.add_row([pdName,int(AODFileSizeGB),thisMaxSize,int(nEventsK),thisLumis,AODEventSize,FileSizePerLumi])
   
    if(MaxFileSize < thisMaxSize):
        MaxFileSize = thisMaxSize

    if(breakDebug):
	break   # break out of PD names loop after only one file
    if(break2Debug and countPDs == 2):
        break   # break out of PD names loop after two files

averageEventSize = totalAODSize*1.0e3/totalAODEvents
if(totalLumis != 0):
    averageFileSizePerLumi = totalAODSize/totalLumis
else:
    averageFileSizePerLumi = 0

aTotalAodSize = locale.format("%d", int(totalAODSize), grouping=True)
aTotalEventsK = locale.format("%d", int(totalAODEvents/1.0e03), grouping=True)
aTotalLumis = locale.format("%d", totalLumis, grouping=True)
x.add_row(['Total AOD',aTotalAodSize,MaxFileSize,aTotalEventsK,aTotalLumis,averageEventSize,averageFileSizePerLumi]) 
forCSVx.add_row(['Total AOD',int(totalAODSize),MaxFileSize,int(totalAODEvents/1.0e3),totalLumis,averageEventSize,averageFileSizePerLumi]) 

print "\n AOD statistics for Run2015E-PromptReco-v1 datasets in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print >> fileOut, "\n AOD statistics for Run2015E-PromptReco-v1 datasets in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print x
print >> fileOut, forCSVx

print "\n AOD File Summary:"
print >> fileOut, "\n AOD File Summary:"
print " Total Volume (GB)= ", aTotalAodSize
print >> fileOut, " Total Volume (GB)= ", aTotalAodSize
aTotalEvents = locale.format("%d", totalAODEvents, grouping=True)
print " Number of Events = ", aTotalEvents
print >> fileOut, " Number of Events = ", aTotalEvents
print " Event Size (MB/Event) = ", 
print >> fileOut, " Event Size (MB/Event) = ", 
print "%0.3f" % (averageEventSize)
print " Number of Lumis = ", aTotalLumis
print >> fileOut, " Number of Lumis = ", aTotalLumis
print " Lumi Size (GB/Lumi) = ",
print >> fileOut, " Lumi Size (GB/Lumi) = ",
print "%0.3f" % (averageFileSizePerLumi)
print >> fileOut, "%0.3f" % (averageFileSizePerLumi)
print "\n"
print >> fileOut, "\n"

fileOut.close()

exit()
