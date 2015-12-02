fileInput = open('lumicounts.txt','r')
for line in fileInput:
	nLumis = line.rstrip('\n')
	print "1) nLumis ", nLumis
	thisLumis = int(nLumis.strip('count(lumi)='))
	print "2) thisLumis ", thisLumis

print "exiting"
exit()
