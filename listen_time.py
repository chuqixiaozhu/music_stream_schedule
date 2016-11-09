import csv
import sys
import datetime

with open('../data/user_000001_small.tsv', newline='') as user_data_in,\
     open('../data/user_000001_listen_time.tsv', 'w') as user_listen_time_out:
     user_data_in = csv.reader(user_data_in, delimiter='\t')
     first_line_flag = True
    for record_now in user_data_in: # Corrent line: record_now
        if first_line_flag:
            first_line_flag = False
            record_last = record_now # Sceond line: record_last
            continue

        # Get two timestamps of now and last time, respectively
        origin_time_now = record_now[1]
        origin_time_last = record_last[1]
        datetime_now = datetime.datetime(int(origin_time_now[:4]),\
                                 int(origin_time_now[5:7]),\
                                 int(origin_time_now[8:10]),\
                                 int(origin_time_now[11:13]),\
                                 int(origin_time_now[14:16]),\
                                 int(origin_time_now[17:19]))
        datetime_last = datetime.datetime(int(origin_time_last[:4]),\
                                  int(origin_time_last[5:7]),\
                                  int(origin_time_last[8:10]),\
                                  int(origin_time_last[11:13]),\
                                  int(origin_time_last[14:16]),\
                                  int(origin_time_last[17:19]))

        # Computer listen time
        listen_time = (datetime_last - datetime_now)\
                 / datetime.timedelta(milliseconds=1)

        # Write results to the output file
        new_combine = [record_now[0], str(listen_time)]\
                   + record_now[2:]
        record_new = '\t'.join(new_combine)
        user_listen_time_out.write(record_new + '\n')
        record_last = record_now





