import csv
import sys

csv.field_size_limit(sys.maxsize)
with open('/scratch/zpeng.scratch/Dropbox/PhD/works/homeworks/634 Advanced Computer Networking/network project/music data set---lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv', newline='') as tsvin,\
	 open('user_000001.tsv', 'w') as tsvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    # tsvout = csv.writer(tsvout)

    for row in tsvin:
        if row[0] == 'user_000001':
        	record = str(row[0])
        	for column in row[1:]:
        		record += '\t' + str(column)
        	# tsvout.writerow(record)
        	tsvout.write(record + '\n')
        	tsvout.flush()
        	# print('record = ', record)