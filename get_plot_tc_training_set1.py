import os
#import matplotlib.pyplot as plt

address = 'results_txt/'
accuracy_file = address + 'accuracy1_training.txt'
precision_file = address + 'precision_training.txt'
recall_file = address + 'recall_training.txt'
f1_file = address + 'f1_training.txt'

def write2file(file_name, user_id, num_str):
    with open(file_name, 'a') as fout:
        fout.write(user_id + ' ' + num_str + '\n')

def get_all_results(file, userid):
    # location = 3
    accuracy1_loc = 1
    precision_loc = 2
    recall_loc = 3
    f1_loc = 4

    with open(file, 'r') as fin:
        i = 0
        for line in fin:
            i += 1
            words = line.split()
            num_str = words[-1]
            if i == accuracy1_loc:
                accuracy1 = num_str
                write2file(accuracy_file, userid, accuracy1)
            elif i == precision_loc:
                precision = num_str
                write2file(precision_file, userid, precision)
            elif i == recall_loc:
                recall = num_str
                write2file(recall_file, userid, recall)
            elif i == f1_loc:
                f1_score = num_str
                write2file(f1_file, userid, f1_score)

def clear_files():
    with open(accuracy_file, 'w') as fout:
        pass
    with open(precision_file, 'w') as fout:
        pass
    with open(recall_file, 'w') as fout:
        pass
    with open(f1_file, 'w') as fout:
        pass

def extract_data():
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&two_half&ue/'
    # result_file = 'skip_precision_two_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&half&ue/'
    # result_file = 'skip_precision_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_partition/'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/tc_of_training_set1/'
    # with open(result_file, 'w') as fout:
    clear_files()
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    for file_name in data_files:
        if file_name[-4:] != '.txt':
            continue
        file = data_address_prefix + file_name
        user_id = file_name[5:11]
        # skip_precision = get_skip_precision(file, user_id)
        # fout.write(user_id + ' ' + skip_precision + '\n')
        get_all_results(file, user_id)

if __name__ == '__main__':
    extract_data()

