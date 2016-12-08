import numpy as np
from sklearn import mixture
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
# import matplotlib.pyplot as plt
#import cv2
import csv
import os
from get_marks import get_marks
from get_marks import is_same_interval
from get_marks import get_label
from table_of_confussion import get_table_of_confussion 
from start_time_label import get_start_time_label

# sp_index = 0

def predict_bivar_judge_with_error(in_file, in_filename, out_address):
    # tansfer string to number so that we can train
    data = []
    # track_time_all = []
    # with open('/scratch/zpeng.scratch/pppp/music/data/listen/user_000002_time.tsv') as f:
    with open(in_file, 'r') as f:
        for line in f:
            # song,l,artist,percentage,a4,a5,a6 = line.split(",")
            userid,start,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
            # track_time_all.append(float(tt)/1000)
            if float(percentage) > 1:
                continue
            start_label = get_start_time_label(start)
            bb = [bin(ord(c))[2:] for c in song]
            px = 0
            for item in bb:
                px = int(item)^px
            px = float(px)/100

            cc = [bin(ord(c))[2:] for c in artist]
            py = 0
            for item in cc:
                py = int(item)^py
            py = float(py)/100

            # if float(percentage) > 1.0:
            #     percentage = '1.0' # 1 means non-skip

            data.append([float(px),float(py),float(start_label),percentage])
            # data.append([percentage,float(px),float(py),float(start_label)])

    #training two randomforestregressor models, one for judge whether it is 1 or 0, the other is used to judge the specific number less than zero
    data = np.asarray(data,dtype='float')
    # estimator = RandomForestRegressor(n_estimators = 100) # origin

    ###################################################
    # 1n Classifier Training
    ###################################################
    train_start = 0
    train_end = int(np.floor(data.shape[0] * 2/3))
    # train_end = int(np.floor(data.shape[0] * 9/10))
    zero_y = data.copy()

    # label: 0 means Skip, label_max means Non-Skip
    marks = get_marks(count=10, lower=0, upper=1)
    label_max = len(marks) - 1
    for i in range(zero_y.shape[0]):
        # sp = zero_y[i,2]
        sp = zero_y[i,-1]
        label = get_label(sp, marks)
        if label != label_max:
            label = 0 # 0 means Skip
        # zero_y[i,2] = label
        zero_y[i,-1] = label
    # /label
    estimator = RandomForestClassifier(n_estimators = 100)
    try:
        # estimator.fit(data[train_start:train_end,:2],y = zero_y[train_start:train_end,2])
        estimator.fit(data[train_start:train_end,:-1],y = zero_y[train_start:train_end,-1])
    except:
        print("Exception: the 1st training failed.")
        return

    ###################################################
    # Testing for the 1st training set
    ###################################################
    try:
        result_training1 = estimator.predict(zero_y[train_start:train_end,:-1])
    except:
        print("Exception: the testing for 1st training set failed.")
        return

    ###################################################
    # Calculate the Confusion Matrix for 1st training test
    ###################################################
    A = zero_y[train_start:train_end,-1]
    P = result_training1
    tc = get_table_of_confussion(A, P)
    tp = tc['TP'] # True Positive 
    tn = tc['TN'] # True Negative
    fp = tc['FP'] # False Positive
    fn = tc['FN'] # False Negative
    accuracy = (tp + tn) / len(P)
    if tp == 0 and fp == 0:
        precision = -1
    else:
        precision = tp / (tp + fp)
    if tp + fn == 0:
        recall = -1
    else:
        recall = tp / (tp + fn)
    if 2*tp + fp + fn == 0:
        f1_score = -1
    else:
        f1_score = 2*tp / (2*tp + fp + fn)
    tmp_str = 'Training set1: Accuracy: ' + str(accuracy) + '\n' + \
                'Precision: ' + str(precision) + '\n' + \
                'Recall: ' + str(recall) + '\n' + \
                'F1 Score: ' + str(f1_score)
    print(tmp_str)
    discript = tmp_str

    ###################################################
    # Plot a figure
    ###################################################
    # file_name = in_filename[:-9]
    file_name = in_filename[:11]
    out_file_text = out_address + file_name + '_training_set1_tc.txt'
    with open(out_file_text, 'w') as output:
        output.write(discript)
    # out_file_png = out_address + file_name + '_bi_predict_with_error.png'
    # plt.savefig(out_file_png)

if __name__ == '__main__':
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen_tmp/'
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/time_and_skip/'
    # result_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_partition/'
    result_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/tc_of_training_set1/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    for file in data_files:
        file_in = data_address_prefix + file
        print("in:", file_in)
        predict_bivar_judge_with_error(file_in, file, result_address_prefix)

