import csv
from get_duration import get_duration

with open('../data/user_000001_small.tsv', newline='') as user_data_in,\
     open('../data/user_000001_music_duration.tsv', 'w') as music_duration_out:
     user_data_in = csv.reader(user_data_in, delimiter='\t')
     for record in user_data_in: # Corrent line: record_now
        mbid = record[4]
        artist = record[3]
        track = record[5]
        duration = get_duration(mbid, artist, track)
        # duration = get_duration(artist=artist, track=track)
        new_record = record + list(str(duration))
        line = '\t'.join(new_record)
        music_duration_out.write(line + '\n')
