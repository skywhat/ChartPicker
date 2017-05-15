import csv

writer=csv.writer(file('your.csv','wb'))
writer.writerow(['Column1','Column2','Column3'])
lines=[range(3) for i in range(5)]
for line in lines:
    writer.writerow(line)