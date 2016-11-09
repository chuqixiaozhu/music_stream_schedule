import csv
import sys

# csv.field_size_limit(sys.maxsize)
# with open('/scratch/zpeng.scratch/Dropbox/PhD/works/homeworks/634 Advanced Computer Networking/network project/music data set---lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv', newline='') as tsvin,\
# 	 open('../data/user_000001.tsv', 'w') as tsvout:
#     tsvin = csv.reader(tsvin, delimiter='\t')
#     # tsvout = csv.writer(tsvout)

#     for row in tsvin:
#         if row[0] == 'user_000001':
#         	record = str(row[0])
#         	for column in row[1:]:
#         		record += '\t' + str(column)
#         	# tsvout.writerow(record)
#         	tsvout.write(record + '\n')
#         	tsvout.flush()
#         	# print('record = ', record)

csv.field_size_limit(sys.maxsize)
with open('/scratch/zpeng.scratch/Dropbox/PhD/works/homeworks/634 Advanced Computer Networking/network project/music data set---lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv', newline='') as datain:
# with open('../data/user_000001_small.tsv', newline='') as datain:
    datain = csv.reader(datain, delimiter='\t')

    last_row = ''
    is_firstline = True
    count = 0
    for now_row in datain:
        user_id = now_row[0]
        if is_firstline:
            last_row = now_row
            is_firstline = False
            dataout = open('../data/users/' + now_row[0] + '.tsv', 'w')
            line = '\t'.join(now_row)
            dataout.write(line + '\n')
            continue

        if user_id != last_row[0]:
            last_row = now_row
            dataout.close()
            dataout = open('../data/users/' + now_row[0] + '.tsv', 'w')
            line = '\t'.join(now_row)
            dataout.write(line + '\n')
            continue

        last_row = now_row
        line = '\t'.join(now_row)
        dataout.write(line + '\n')

        count += 1
        if count % 10000 == 0:
            print('.', end='', flush=True)
