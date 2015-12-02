#!/usr/bin/env pytho/
#
# Script to print information about the AOD pp Reference Run PDs in DAS in table format
# Composed by Hong Ni and Charles Maguire
#
 
from datetime import datetime
import os
from prettytable import PrettyTable
from prettytable import ALL
import locale      # for printing location specific separators (comma or decimal point) for large integers
locale.setlocale(locale.LC_ALL, 'en_US')

#Dir = "/afs/cern.ch/user/h/honi/CMSSW_7_5_5_patch3/src/PythonScript_pprefEvtVolumeSizeForPDs/AOD"
#Dir = "/gpfs21/scratch/maguire/CMSSW_7_5_5_patch3/src/Run2015Monitoring/MyProject/PythonScript_pprefEvtVolumeSizeForPDs/AOD/"
Dir = "."   # use present working directory

breakDebug = False   # will process only the first PD
break2Debug = False  # will process only the first and second PDs (these are minimum bias)
break22Debug = False  # will process only the first 22 PDs (these are minimum bias plus two other)
countTwoMinBias = False  # count only the 2 minimum bias PDs and the other PDs
countMinBias = False  # count only the 20 minimum bias PDs
countOther = False    # count only the not minimum bias PDs
printDebug = False

fileOut = open("forCSV_output_printppPDsinDAS_AOD.txt", "w")

pdNames = ["MinimumBias1"]
pdNames.append("MinimumBias2")
pdNames.append("MinimumBias3")
pdNames.append("MinimumBias4")
pdNames.append("MinimumBias5")
pdNames.append("MinimumBias6")
pdNames.append("MinimumBias7")
pdNames.append("MinimumBias8")
pdNames.append("MinimumBias9")
pdNames.append("MinimumBias10")
pdNames.append("MinimumBias11")
pdNames.append("MinimumBias12")
pdNames.append("MinimumBias13")
pdNames.append("MinimumBias14")
pdNames.append("MinimumBias15")
pdNames.append("MinimumBias16")
pdNames.append("MinimumBias17")
pdNames.append("MinimumBias18")
pdNames.append("MinimumBias19")
pdNames.append("MinimumBias20")
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

xMinBias = PrettyTable(["PD Name","File Vol. (GB)","Max Lumi (GB)","Events (K)","Lumis","Evt Size (MB/Evt)","Lumi Size (GB/LS)"])
xMinBias.align["PD Name"] = "l"
xMinBias.padding_width = 1
xMinBias.float_format = .3;
xMinBias.hrules = ALL

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

totalMinBiasAODSize = 0
totalMinBiasAODEvents = 0
totalMinBiasLumis = 0
MaxMinBiasFileSize = 0

countPDs = 0
for pdName in pdNames:
    countPDs += 1

    if(countMinBias and countPDs > 20):
         break
    if(countTwoMinBias == False and countOther and countPDs < 21):
         continue
    if(countTwoMinBias and countPDs > 2 and countPDs < 21):
         continue

    print "Processing AOD dataset PD", pdName, "with countPDs", countPDs

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
        if(countPDs < 21):
	    totalMinBiasAODEvents += thisEvents

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
        if(countPDs < 21):
	    totalMinBiasAODSize += AODFileSizeGB

    fileInput.close()

    countLumiAODCommand = Dir + '/das.py --limit=1000 --format=plain --query="run,lumi dataset=' + dasAODPathName + ' | count(lumi)" > tmp.txt ; tail -1 tmp.txt > lumicounts.txt'
    if(printDebug): print "countLumiAODCommand: ", countLumiAODCommand
    os.system(countLumiAODCommand)
    fileInput = open('lumicounts.txt','r')
    thisLumis = 0
    for line in fileInput:
        nLumis = line.strip('count(lumi)=N/A')
        if(nLumis != '[]'):
            thisLumis = int(nLumis)
        else:
            nLumis = 0
        totalLumis += thisLumis
        if(countPDs < 21):
	    totalMinBiasLumis += thisLumis

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

    if(countPDs > 20):
        x.add_row([pdName,aAODFileSizeGB,thisMaxSize,aEventsK,aLumis,AODEventSize,FileSizePerLumi])
        if(MaxFileSize < thisMaxSize):
            MaxFileSize = thisMaxSize
    else:
        xMinBias.add_row([pdName,aAODFileSizeGB,thisMaxSize,aEventsK,aLumis,AODEventSize,FileSizePerLumi])
        if(MaxMinBiasFileSize < thisMaxSize):
            MaxMinBiasFileSize = thisMaxSize

    forCSVx.add_row([pdName,int(AODFileSizeGB),thisMaxSize,int(nEventsK),thisLumis,AODEventSize,FileSizePerLumi])

    if(breakDebug):
	break   # break out of PD names loop after only one file
    if(break2Debug and countPDs == 2):
        break   # break out of PD names loop after two files
    if(break22Debug and countPDs == 22):
        break   # break out of PD names loop after twelve files
    if(countMinBias and countPDs == 20):
        break   # break out of PD names loop after processing only Minimum Bias files 

averageEventSize = totalAODSize*1.0e3/totalAODEvents
if(totalLumis != 0):
    averageFileSizePerLumi = totalAODSize/totalLumis
else:
    averageFileSizePerLumi = 0

averageMinBiasEventSize = 0
if(totalMinBiasAODEvents > 0): averageMinBiasEventSize = totalMinBiasAODSize*1.0e3/totalMinBiasAODEvents
averageMinBiasFileSizePerLumi = 0
if(totalMinBiasLumis > 0): averageMinBiasFileSizePerLumi = totalMinBiasAODSize/totalMinBiasLumis

aMinBiasAodSize = locale.format("%d", int(totalMinBiasAODSize), grouping=True)
aMinBiasEventsK = locale.format("%d", int(totalMinBiasAODEvents/1.0e03), grouping=True)
aMinBiasLumis = locale.format("%d", totalMinBiasLumis, grouping=True)

#
# Need to subtract min bias numbers from the total numbers in order to get the not minimum bias totals
#
averageOtherEventSize = 0
if(totalAODEvents-totalMinBiasAODEvents > 0): averageOtherEventSize = (totalAODSize-totalMinBiasAODSize)*1.0e3/(totalAODEvents-totalMinBiasAODEvents)
averageOtherFileSizePerLumi = 0
if(totalLumis-totalMinBiasLumis > 0): averageOtherFileSizePerLumi = (totalAODSize-totalMinBiasAODSize)/(totalLumis-totalMinBiasLumis)

aOtherAodSize = locale.format("%d", int(totalAODSize-totalMinBiasAODSize), grouping=True)
aOtherEventsK = locale.format("%d", int((totalAODEvents-totalMinBiasAODEvents)/1.0e03), grouping=True)
aOtherLumis = locale.format("%d", (totalLumis-totalMinBiasLumis), grouping=True)

aTotalAodSize = locale.format("%d", int(totalAODSize), grouping=True)
aTotalEventsK = locale.format("%d", int(totalAODEvents/1.0e03), grouping=True)
aTotalLumis = locale.format("%d", totalLumis, grouping=True)

x.add_row(['Total Other',aOtherAodSize,MaxFileSize,aOtherEventsK,aOtherLumis,averageOtherEventSize,averageOtherFileSizePerLumi]) 
xMinBias.add_row(['Total MinBias',aMinBiasAodSize,MaxMinBiasFileSize,aMinBiasEventsK,aMinBiasLumis,averageMinBiasEventSize,averageMinBiasFileSizePerLumi]) 

forCSVx.add_row(['Total AOD',int(totalAODSize),MaxFileSize,int(totalAODEvents/1.0e3),totalLumis,averageEventSize,averageFileSizePerLumi]) 

print >> fileOut, "\n Statistics for Run2015E-PromptReco-v1 AOD PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville, 7 hours earlier than CET)"
print >> fileOut, forCSVx

print "\n Statistics for Run2015E-PromptReco-v1 AOD PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville, 7 hours earlier than CET)"
print xMinBias
if(countMinBias):
    exit()	
print "\n Statistics for Run2015E-PromptReco-v1 AOD PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville, 7 hours earlier than CET)"
print x
if(countOther):
    exit()	

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
