import csv
from feature_extract import FeatureFinder

fobj = FeatureFinder()
fbull = open('databull.txt', 'wb')
fbear = open('databear.txt', 'wb')
fneut = open('dataneut.txt', 'wb')
with open('dataset.csv', 'r',  encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #print(row)
        try:
            row = row[0].split(';')
        except:
            continue
        #print(row)
        try:
            if row[3] == 'negative':
                line = fobj.processTweet(row[2])+'\n'
                fbear.write(line.encode('utf8'))
            if row[3] == 'positive':
                line = fobj.processTweet(row[2]) + '\n'
                fbull.write(line.encode('utf8'))
            if row[3] == 'neutral':
                line = fobj.processTweet(row[2]) + '\n'
                fneut.write(line.encode('utf8'))
        except:
            continue
csvfile.close()
fbull.close()
fbear.close()
fneut.close()