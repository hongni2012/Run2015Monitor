fileInput = open('output_printppPDsinDAS_AOD.txt', 'r')

result = []
for line in fileInput:
    splitdata = line.split("|")
    if len(splitdata) == 1:
        continue  # skip lines with no separators
    linedata = []
    for field in splitdata:
        field = field.strip()
        if field:
            linedata.append(field)
    result.append(linedata)

fileOutput = open('csvformat_ppPDsinDAS_AOD.csv','w')
for item in result:
    mergeditem = Column = ','.join(item)  
    fileOutput.write(mergeditem)
    fileOutput.write('\n')
fileOutput.close() 
