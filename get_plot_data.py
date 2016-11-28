import os
#import matplotlib.pyplot as plt

def write2file(file_name, user_id, num_str):
    with open(file_name, 'a') as fout:
        fout.write(user_id + ' ' + num_str + '\n')

def get_all_results(file, userid):
    # location = 3
    accuracy_loc = 1
    precision_loc = 2
    recall_loc = 3
    f1_loc = 4
    skip_accuracy_loc = 5
    user_exp_loc = 6

    accuracy_file = 'accuracy.txt'
    precision_file = 'precision.txt'
    recall_file = 'recall.txt'
    f1_file = 'f1.txt'
    skip_accuracy_file = 'skip_accuracy.txt'
    user_exp_file = 'user_exp.txt'

    with open(file, 'r') as fin:
        i = 0
        for line in fin:
            i += 1
            words = line.split()
            num_str = words[-1]
            if i == accuracy_loc:
                accuracy = num_str
                write2file(accuracy_file, userid, accuracy)
            elif i == precision_loc:
                precision = num_str
                write2file(precision_file, userid, precision)
            elif i == recall_loc:
                recall = num_str
                write2file(recall_file, userid, recall)
            elif i == f1_loc:
                f1_score = num_str
                write2file(f1_file, userid, f1_score)
            elif i == skip_accuracy_loc:
                skip_accuracy = num_str
                write2file(skip_accuracy_file, userid, skip_accuracy)
            elif i == user_exp_loc:
                user_exp = num_str
                write2file(user_exp_file, userid, user_exp)

def clear_files():
    accuracy_file = 'accuracy.txt'
    precision_file = 'precision.txt'
    recall_file = 'recall.txt'
    f1_file = 'f1.txt'
    skip_accuracy_file = 'skip_accuracy.txt'
    user_exp_file = 'user_exp.txt'

    with open(accuracy_file, 'w') as fout:
        pass
    with open(precision_file, 'w') as fout:
        pass
    with open(recall_file, 'w') as fout:
        pass
    with open(f1_file, 'w') as fout:
        pass
    with open(skip_accuracy_file, 'w') as fout:
        pass
    with open(user_exp_file, 'w') as fout:
        pass


def extract_data():
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&two_half&ue/'
    # result_file = 'skip_precision_two_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&half&ue/'
    # result_file = 'skip_precision_half.txt'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_partition/'
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

