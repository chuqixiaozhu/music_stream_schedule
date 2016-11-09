import csv
import datetime
from get_duration import get_duration

# with open('../data/user_000001_small.tsv', newline='') as user_data_in,\
#      open('../data/user_000001_music_duration.tsv', 'w') as music_duration_out:
with open('../data/user_000001.tsv', newline='') as user_data_in,\
     open('../data/user_000001_with_listen_duration.tsv', 'w') as user_data_out:
    user_data_in = csv.reader(user_data_in, delimiter='\t')
    count = 0
    first_line_flag = True
    for record_now in user_data_in: # Corrent line: record_now
        if first_line_flag:
        # If is the first line of records
            first_line_flag = False
            record_last = record_now # Sceond line: record_last
            continue

        # Get two timestamps of now and last time, respectively
        origin_time_now = record_now[1]
        origin_time_last = record_last[1]
        record_last = record_now
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
        # Computer music length
        mbid = record_now[4]
        artist = record_now[3]
        track = record_now[5]
        music_length = get_duration(mbid, artist, track)
        if music_length == '0' or music_length == '?':
            continue
        # duration = get_duration(artist=artist, track=track)
        # new_record = record + list(str(duration))
        # record.append(str(music_duration))    

        # Computer listen time
        listen_time = (datetime_last - datetime_now)\
                 / datetime.timedelta(milliseconds=1)

        # Computer skip point
        # print("@50 music_length =", music_length) #test
        skip_point = listen_time / float(music_length)

        new_combine = [record_now[0], str(listen_time), str(music_length),\
                       str(skip_point)] + record_now[2:]
        line = '\t'.join(new_combine)
        user_data_out.write(line + '\n')
        count += 1
        if count % 10 == 0:
            print('.', end='', flush=True)

