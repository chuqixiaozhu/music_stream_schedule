from durations import durations
import os

def user_listen_time():
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/users/'
    result_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    data_files = os.listdir(data_address_prefix)
    data_files = sorted(data_files)
    for file in data_files:
        file_in = data_address_prefix + file
        file_out = result_address_prefix + file[:-4] + '_time' + '.tsv'
        print("in:", file_in, "out:", file_out)
        durations(file_in, file_out)
        print('\n')

if __name__ == '__main__':
    user_listen_time()