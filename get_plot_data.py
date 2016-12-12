import os
#import matplotlib.pyplot as plt

address = 'results_txt/'
accuracy_file = address + 'accuracy1.txt'
precision_file = address + 'precision.txt'
recall_file = address + 'recall.txt'
f1_file = address + 'f1.txt'
accuracy2_file = address + 'accuracy2.txt'
overall_accuray_file = address + 'overall_accuracy.txt'
user_exp_file = address + 'user_exp.txt'
saved_energy_ratio_file = address + 'saved_energy_ratio.txt'
saved_energy_ratio_naive_file = address + 'saved_energy_ratio_naive.txt'

accuracy1_loc = 1
precision_loc = 2
recall_loc = 3
f1_loc = 4
accuracy2_loc = 5
overall_accuracy_loc = 6
user_exp_loc = 7
saved_energy_ratio_loc = 8
saved_energy_ratio_naive_loc = 9

def write2file(file_name, user_id, num_str):
    with open(file_name, 'a') as fout:
        fout.write(user_id + ' ' + num_str + '\n')

def get_all_results(file, userid):
    # location = 3

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
            elif i == accuracy2_loc:
                accuracy2 = num_str
                write2file(accuracy2_file, userid, accuracy2)
            elif i == overall_accuracy_loc:
                overall_accuray = num_str
                write2file(overall_accuray_file, userid, overall_accuray)
            elif i == user_exp_loc:
                user_exp = float(num_str)
                user_exp = 1 - user_exp
                write2file(user_exp_file, userid, str(user_exp))
            elif i == saved_energy_ratio_loc:
                saved_energy_ratio = num_str
                write2file(saved_energy_ratio_file, userid, saved_energy_ratio)
            elif i == saved_energy_ratio_naive_loc:
                saved_energy_ratio_naive = num_str
                write2file(saved_energy_ratio_naive_file, userid, saved_energy_ratio_naive)

def clear_files():

    with open(accuracy_file, 'w') as fout:
        pass
    with open(precision_file, 'w') as fout:
        pass
    with open(recall_file, 'w') as fout:
        pass
    with open(f1_file, 'w') as fout:
        pass
    with open(accuracy2_file, 'w') as fout:
        pass
    with open(overall_accuray_file, 'w') as fout:
        pass
    with open(user_exp_file, 'w') as fout:
        pass
    with open(saved_energy_ratio_file, 'w') as fout:
        pass
    with open(saved_energy_ratio_naive_file, 'w') as fout:
        pass


def extract_data():
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&two_half&ue/'
    # result_file = 'skip_precision_two_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error_20161119_abs&half&ue/'
    # result_file = 'skip_precision_half.txt'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_partition/'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_start_time/'
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

