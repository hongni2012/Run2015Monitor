#!/usr/bin/env pytho/
#
# Script to print information about the RAW pp Reference Run PDs in DAS in table format
# Composed by Hong Ni and Charles Maguire
#
 
from datetime import datetime
import os
from prettytable import PrettyTable
from prettytable import ALL
import locale      # for printing location specific separators (comma or decimal point) for large integers
locale.setlocale(locale.LC_ALL, 'en_US')

Dir = "."   # use present working directory

breakDebug = False   # will process only the first PD
break2Debug = False  # will process only the first and second PDs (these are minimum bias)
break22Debug = False  # will process only the first 22 PDs (these are minimum bias plus two other)
countTwoMinBias = False  # count only the 2 minimum bias PDs and the other PDs
countMinBias = False  # count only the 20 minimum bias PDs
countOther = False    # count only the not minimum bias PDs
printDebug = False

fileOut = open("forCSV_output_printppPDsinDAS_RAW.txt", "w")

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
 
totalRAWSize = 0
totalRAWEvents = 0
totalLumis = 0
MaxFileSize = 0

totalMinBiasRAWSize = 0
totalMinBiasRAWEvents = 0
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

    print "Processing RAW dataset PD", pdName, "with countPDs", countPDs

    dasRAWPathName = '/' + pdName + '/Run2015E-v1/RAW'
    findEventsRAWCommand = Dir + '/das.py --limit=1000 --format=plain --query="dataset dataset=' + dasRAWPathName + ' | grep dataset.nevents" > tmp.txt ; tail -1 tmp.txt > events.txt'
    if(printDebug): print "findEventsRAWCommand: ", findEventsRAWCommand
    os.system(findEventsRAWCommand)
    fileInput = open('events.txt', 'r')
    thisEvents = 0
    RAWEventSize = 0
    nEventsK = 0
    for line in fileInput:
        nEvents = line.rstrip('\n')
        if(nEvents != '[]'):
            nEventsK = int(nEvents)/1.0e3 
            thisEvents = int(nEvents)
        else:
            nEvents = 0
            nEventsK = 0
        totalRAWEvents += thisEvents
        if(countPDs < 21):
	    totalMinBiasRAWEvents += thisEvents

    fileInput.close()
 
    findSizeRAWCommand = Dir + '/das.py --limit=1000 --format=plain --query="dataset dataset=' + dasRAWPathName + ' | grep dataset.size" > tmp.txt ; tail -1 tmp.txt > size.txt'
    if(printDebug): print "findSizeRAWCommand: ", findSizeRAWCommand
    os.system(findSizeRAWCommand)
    fileInput = open('size.txt', 'r')
    RAWFileSizeGB = 0
    for line in fileInput:
        RAWFileSize = line.rstrip('\n')
        if(RAWFileSize == '[]'):
            RAWFileSizeGB = 0
        else:
            RAWFileSizeGB = int(RAWFileSize)/1.0e9
            if(thisEvents > 0):
               RAWEventSize = RAWFileSizeGB*1.0e3/thisEvents
        totalRAWSize += RAWFileSizeGB
        if(countPDs < 21):
	    totalMinBiasRAWSize += RAWFileSizeGB

    fileInput.close()

    countLumiRAWCommand = Dir + '/das.py --limit=1000 --format=plain --query="run,lumi dataset=' + dasRAWPathName + ' | count(lumi)" > tmp.txt ; tail -1 tmp.txt > lumicounts.txt'
    if(printDebug): print "countLumiRAWCommand: ", countLumiRAWCommand
    os.system(countLumiRAWCommand)
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
        FileSizePerLumi = RAWFileSizeGB/thisLumis
    fileInput.close()

    findMaxFileRAWCommand = Dir + '/das.py --limit=1000 --format=plain --query="file dataset=' + dasRAWPathName + ' | max(file.size)" > tmp.txt ; tail -1 tmp.txt > maxfilesize.txt'
    if(printDebug): print "findMaxFileRAWCommand: ", findMaxFileRAWCommand
    os.system(findMaxFileRAWCommand)
    fileInput = open('maxfilesize.txt','r')
    thisMaxSize = 0
    for line in fileInput:
        maxsize = line.strip('max(file.size)=')
        if(maxsize != '[]'):    
            thisMaxSize = int(maxsize)/1.0e9
    fileInput.close()
   
    aRAWFileSizeGB = locale.format("%d", int(RAWFileSizeGB), grouping=True)
    aEventsK = locale.format("%d", int(nEventsK), grouping=True)
    aLumis = locale.format("%d", thisLumis, grouping=True)

    if(countPDs > 20):
        x.add_row([pdName,aRAWFileSizeGB,thisMaxSize,aEventsK,aLumis,RAWEventSize,FileSizePerLumi])
        if(MaxFileSize < thisMaxSize):
            MaxFileSize = thisMaxSize
    else:
        xMinBias.add_row([pdName,aRAWFileSizeGB,thisMaxSize,aEventsK,aLumis,RAWEventSize,FileSizePerLumi])
        if(MaxMinBiasFileSize < thisMaxSize):
            MaxMinBiasFileSize = thisMaxSize

    forCSVx.add_row([pdName,int(RAWFileSizeGB),thisMaxSize,int(nEventsK),thisLumis,RAWEventSize,FileSizePerLumi])

    if(breakDebug):
	break   # break out of PD names loop after only one file
    if(break2Debug and countPDs == 2):
        break   # break out of PD names loop after two files
    if(break22Debug and countPDs == 22):
        break   # break out of PD names loop after twelve files
    if(countMinBias and countPDs == 20):
        break   # break out of PD names loop after processing only Minimum Bias files 

averageEventSize = totalRAWSize*1.0e3/totalRAWEvents
if(totalLumis != 0):
    averageFileSizePerLumi = totalRAWSize/totalLumis
else:
    averageFileSizePerLumi = 0

averageMinBiasEventSize = 0
if(totalMinBiasRAWEvents > 0): averageMinBiasEventSize = totalMinBiasRAWSize*1.0e3/totalMinBiasRAWEvents
averageMinBiasFileSizePerLumi = 0
if(totalMinBiasLumis > 0): averageMinBiasFileSizePerLumi = totalMinBiasRAWSize/totalMinBiasLumis

aMinBiasRawSize = locale.format("%d", int(totalMinBiasRAWSize), grouping=True)
aMinBiasEventsK = locale.format("%d", int(totalMinBiasRAWEvents/1.0e03), grouping=True)
aMinBiasLumis = locale.format("%d", totalMinBiasLumis, grouping=True)

#
# Need to subtract min bias numbers from the total numbers in order to get the not minimum bias totals
#
averageOtherEventSize = 0
if(totalRAWEvents-totalMinBiasRAWEvents > 0): averageOtherEventSize = (totalRAWSize-totalMinBiasRAWSize)*1.0e3/(totalRAWEvents-totalMinBiasRAWEvents)
averageOtherFileSizePerLumi = 0
if(totalLumis-totalMinBiasLumis > 0): averageOtherFileSizePerLumi = (totalRAWSize-totalMinBiasRAWSize)/(totalLumis-totalMinBiasLumis)

aOtherRawSize = locale.format("%d", int(totalRAWSize-totalMinBiasRAWSize), grouping=True)
aOtherEventsK = locale.format("%d", int((totalRAWEvents-totalMinBiasRAWEvents)/1.0e03), grouping=True)
aOtherLumis = locale.format("%d", (totalLumis-totalMinBiasLumis), grouping=True)

aTotalRawSize = locale.format("%d", int(totalRAWSize), grouping=True)
aTotalEventsK = locale.format("%d", int(totalRAWEvents/1.0e03), grouping=True)
aTotalLumis = locale.format("%d", totalLumis, grouping=True)

x.add_row(['Total Other',aOtherRawSize,MaxFileSize,aOtherEventsK,aOtherLumis,averageOtherEventSize,averageOtherFileSizePerLumi]) 
xMinBias.add_row(['Total MinBias',aMinBiasRawSize,MaxMinBiasFileSize,aMinBiasEventsK,aMinBiasLumis,averageMinBiasEventSize,averageMinBiasFileSizePerLumi]) 

forCSVx.add_row(['Total RAW',int(totalRAWSize),MaxFileSize,int(totalRAWEvents/1.0e3),totalLumis,averageEventSize,averageFileSizePerLumi]) 

print >> fileOut, "\n Statistics for Run2015E-v1 RAW PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print >> fileOut, forCSVx

print "\n Statistics for Run2015E-v1 RAW PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print xMinBias
if(countMinBias):
    exit()	
print "\n Statistics for Run2015E-v1 RAW PDs in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print x
if(countOther):
    exit()	

print "\n RAW File Summary:"
print >> fileOut, "\n RAW File Summary:"
print " Total Volume (GB)= ", aTotalRawSize
print >> fileOut, " Total Volume (GB)= ", aTotalRawSize
aTotalEvents = locale.format("%d", totalRAWEvents, grouping=True)
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
