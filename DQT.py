import glob
import re
import csv
import operator
import sys
file_list=glob.glob("*.csv")
fout = open("DQT1.csv",'a')
fieldnames = ['tablename', 'column','rowcount','blankrowscount','blankrowsPercentage','uniqueValueCount','minChar','maxChar','columnvalue','escapeCharacter']
writer = csv.DictWriter(fout, fieldnames=fieldnames)

for file in file_list:
        f=open(file,'r')
        pattern = re.compile(".*(?=\.csv)")
        filename = pattern.findall(str(f.name))[0]
        reader = csv.reader(f,delimiter=',')
        header = next(reader)
        list1 = list(reader)
        index = 0
        writer.writerow({'tablename':'', 'column':'','rowcount':'','blankrowscount':'','blankrowsPercentage':'','uniqueValueCount':'','columnvalue':''})
        writer.writeheader()
        rowcount = str(len(list1))
        for col in header:
                if index != len(header):
                        blankcount = 0
                        items = {}
                        escapeCharacter = {}
                        charlength = {}
                        rowno = 0
                        for row in list1:
                                if row[index] == '':
                                        blankcount = blankcount +1
                                else:
                                        if row[index] in items:
                                                #items.append(row[index])
                                                items[row[index]] += 1
                                        else:
                                                items[row[index]] = 1
                                        
                                        escapePattern = re.compile(r'\n|\\')
                                        if len(escapePattern.findall(str(row[index]))) != 0:
                                                escapeCharacter[row[index]] = rowno
                                                print str(escapePattern.findall(str(row[index]))) + " : " + str(rowno)
                                rowno = rowno +1
                blankrowpercent = str((float(blankcount)/int(rowcount)*100))
                if blankrowpercent == '0.0':
                        blankrowpercent = '0'
                writer.writerow({'tablename':filename,'column':col,'rowcount':rowcount,'blankrowscount':blankcount,'uniqueValueCount':len(items),'columnvalue':str(sorted(items.items(), key=operator.itemgetter(1), reverse=True))[:50000],'blankrowsPercentage': blankrowpercent,'minChar': str(sorted(items.items(), key= lambda x: len(x[0]), reverse=False))[:500],'maxChar': str(sorted(items.items(), key= lambda x: len(x[0]), reverse=True))[:500] ,'escapeCharacter':str(sorted(escapeCharacter.items(), key=operator.itemgetter(1), reverse=True))[:50000]})
        
                index =index +1
