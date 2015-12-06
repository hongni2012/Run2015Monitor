#!/usr/bin/env pytho/
#
# Script to print information about the RAW PbPb Run PDs in DAS in table format
# Composed by Hong Ni and Charles Maguire
#
 
from datetime import datetime
import os
from prettytable import PrettyTable
from prettytable import ALL
import locale      # for printing location specific delimiters for large integers
locale.setlocale(locale.LC_ALL, 'en_US')

Dir = "."

breakDebug = False  # will process only the first PD
break2Debug = False  # will process only the first and second PDs
printDebug = False

fileOut = open("forCSV_output_printPbPbPDsinDAS_RAW.txt", "w")

pdNames=["HIMinimumBias1"]
pdNames.append("HIMinimumBias2")
pdNames.append("HIMinimumBias3")
pdNames.append("HIMinimumBias4")
pdNames.append("HIMinimumBias5")
pdNames.append("HIMinimumBias6")
pdNames.append("HIMinimumBias7")
pdNames.append("HIForward")
pdNames.append("HIPhoton40AndZ")
pdNames.append("HIEWQExo")
pdNames.append("HIOniaCentral30L2L3")
pdNames.append("HIOniaPeripheral30100")
pdNames.append("HIOniaL1DoubleMu0")
pdNames.append("HIOniaL1DoubleMu0B")
pdNames.append("HIOniaL1DoubleMu0C")
pdNames.append("HIOniaL1DoubleMu0D")
pdNames.append("HIHardProbes")
pdNames.append("HIHardProbesPeripheral")
pdNames.append("HIHardProbesPhotons")
pdNames.append("HIFlowCorr")
pdNames.append("HIOniaTnP")

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
 
totalRAWSize = 0
totalRAWEvents = 0
totalLumis = 0
MaxFileSize = 0

countPDs = 0
for pdName in pdNames:
    countPDs += 1
    print "Processing RAW dataset PD", pdName
    dasRAWPathName = '/' + pdName + '/HIRun2015-v1/RAW'
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
    x.add_row([pdName,aRAWFileSizeGB,thisMaxSize,aEventsK,aLumis,RAWEventSize,FileSizePerLumi])
    forCSVx.add_row([pdName,int(RAWFileSizeGB),thisMaxSize,int(nEventsK),thisLumis,RAWEventSize,FileSizePerLumi])
   
    if(MaxFileSize < thisMaxSize):
        MaxFileSize = thisMaxSize

    if(breakDebug):
	break   # break out of PD names loop after only one file
    if(break2Debug and countPDs == 2):
        break   # break out of PD names loop after two files

averageEventSize = totalRAWSize*1.0e3/totalRAWEvents
if(totalLumis != 0):
    averageFileSizePerLumi = totalRAWSize/totalLumis
else:
    averageFileSizePerLumi = 0

aTotalRawSize = locale.format("%d", int(totalRAWSize), grouping=True)
aTotalEventsK = locale.format("%d", int(totalRAWEvents/1.0e03), grouping=True)
aTotalLumis = locale.format("%d", totalLumis, grouping=True)
x.add_row(['Total RAW',aTotalRawSize,MaxFileSize,aTotalEventsK,aTotalLumis,averageEventSize,averageFileSizePerLumi]) 
forCSVx.add_row(['Total RAW',int(totalRAWSize),MaxFileSize,int(totalRAWEvents/1.0e3),totalLumis,averageEventSize,averageFileSizePerLumi]) 

print "\n RAW statistics for HIRun2015-v1 datasets in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print >> fileOut, "\n RAW statistics for HIRun2015-v1 datasets in DAS at", mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss, "(Nashville time, 7 hours earlier than CET)"
print x
print >> fileOut, forCSVx

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
