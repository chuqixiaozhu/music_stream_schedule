import os
import matplotlib.pyplot as plt

def get_skip_precision(file):
    location = 3
    
    with open(file, 'r') as fin:
        i = 0
        for line in fin:
            i += 1
            if (i == location):
                words = line.split()
                num_str = words[-1]
                precision = num_str[:-1] # remove the '%'
                break

    return precision

def extract_data():
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&two_half&ue/'
    result_file = 'skip_precision_two_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&half&ue/'
    # result_file = 'skip_precision_half.txt'
    with open(result_file, 'w') as fout:
        data_files = os.listdir(data_address_prefix)
        data_files.sort()
        for file_name in data_files:
            if file_name[-4:] != '.txt':
                continue
            file = data_address_prefix + file_name
            user_id = file_name[5:11]
            skip_precision = get_skip_precision(file)
            fout.write(user_id + ' ' + skip_precision + '\n')

if __name__ == '__main__':
    extract_data()

