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

def predict_bivar_judge_with_error(in_file, in_filename, out_address):
    # tansfer string to number so that we can train
    data = []
    # track_time_all = []
    # with open('/scratch/zpeng.scratch/pppp/music/data/listen/user_000002_time.tsv') as f:
    with open(in_file, 'r') as f:
        for line in f:
            # song,l,artist,percentage,a4,a5,a6 = line.split(",")
            userid,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
            # track_time_all.append(float(tt)/1000)
            if float(percentage) > 1:
                continue
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

            data.append([float(px),float(py),percentage])

    #training two randomforestregressor models, one for judge whether it is 1 or 0, the other is used to judge the specific number less than zero
    data = np.asarray(data,dtype='float')
    # estimator = RandomForestRegressor(n_estimators = 100) # origin

    ###################################################
    # 1n Classifier Training
    ###################################################
    train_start = 0
    train_end = int(np.floor(data.shape[0] * 2/3))
    zero_y = data.copy()

    # label
    marks = get_marks(count=10, lower=0, upper=1)
    label_max = len(marks) - 1
    for i in range(zero_y.shape[0]):
        sp = zero_y[i,2]
        label = get_label(sp, marks)
        if label != label_max:
            label = 0 # 0 means Skip
        zero_y[i,2] = label
    # /label
    # estimator = RandomForestClassifier(n_estimators = 100)
    estimator = RandomForestRegressor(n_estimators = 100)
    try:
        estimator.fit(data[train_start:train_end,:2],y = zero_y[train_start:train_end,2])
    except:
        print("Exception: the 1st training failed.")
        return
    ###################################################
    # 2n Classifier Training
    ###################################################
    data_labeled = data.copy()
    for i in range(data_labeled.shape[0]):
        sp = data_labeled[i,2]
        label = get_label(sp, marks)
        data_labeled[i,2] = label

    # Train_index2 should not contain Non-Skip index
    train_index2 = [i for i in range(train_end)]
    for i in range(train_end):
        if data_labeled[i,2] == label_max: # Drop Non-Skip index
            train_index2.remove(i)
    estimator2 = RandomForestClassifier(n_estimators = 100)
    try:
        estimator2.fit(data_labeled[train_index2,:2],\
                        y = data_labeled[train_index2,2])
    except:
        print("Exception: the 2st training failed.")
        return

    ###################################################
    # 1st Predicting phase
    ###################################################
    #result = gmm1.predict(data[300:400,:2])
    # test_start = 22000
    test_start = train_end
    test_end = data.shape[0]
    # test_index = [t for t in xrange(test_start,test_end)]
    test_index1 = [t for t in range(test_start,test_end)]
    try:
        # result = estimator.predict(data[test_index,:2])
        result1 = estimator.predict(zero_y[test_index1,:2])
    except:
        print("Exception: the 1st prediction failed.")
        return
    ################
    # Regression
    ################
    result1 = result1.astype(float)
    # origin
    none_zero_index = np.where(result1 >= label_max/2)
    zero_index = np.where(result1 < label_max/2)
    result1[none_zero_index] = label_max #  means Non-Skip
    result1[zero_index] = 0 # 0 means Skip
    ################
    # /Regression
    ################
    ###################################################
    # Calculate the precision for 1st judgement
    ###################################################
    true_count1 = 0
    good_count1 = 0
    # tmp_str = "precision of 0-1 judge: {0:.1f}%".format(float(counter)/len(test_index)*100)
    # print(tmp_str)
    # discript = tmp_str

    A = zero_y[test_index1,2]
    P = result1
    test_amount1 = len(P)
    for i in range(test_amount1):
        act = A[i]
        pre = P[i]
        if act == pre and pre == label_max:
            true_count1 += 1
        if pre == label_max:
            good_count1 += 1

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
    tmp_str = '0-1 Judge: Accuracy: ' + str(accuracy) + '\n' + \
                'Precision: ' + str(precision) + '\n' + \
                'Recall: ' + str(recall) + '\n' + \
                'F1 Score: ' + str(f1_score)
    print(tmp_str)
    discript = tmp_str

    ###################################################
    # 2n Prediction 
    ###################################################
    # Test_index2 should not contain PREDICTED-Non-Skip index
    test_index2 = test_index1.copy()
    for i in range(len(result1)):
        if result1[i] == label_max: # Drop Non-Skip index
            test_index2.remove(test_start + i)
    try:
        result2 = estimator2.predict(data_labeled[test_index2,:2])
    except:
        print("Exception: the 2nd prediction failed.")
        return
    # result2 = result2.astype(float) # !!!!!!!!!!!!!!!!!!!!!!!
    # error = abs(result2-data[index,2])

    ###################################################
    # Calculate 2nd Predict Accuracy
    ###################################################
    A = data_labeled[test_index2,2]
    P = result2
    test_amount2 = len(P)
    true_count2 = 0
    good_count2 = 0
    # marks = get_marks(count=10, lower=0, upper=1)
    for i in range(test_amount2):
        act = A[i]
        pre = P[i]
        # if is_same_interval(act, pre, marks):
        if act == pre:
            true_count2 += 1
        if pre >= act:
            good_count2 += 1
    # accuracy = true_count2 / test_amount
    true_count = true_count1 + true_count2
    test_amount = test_end - test_start
    accuracy_all = true_count / test_amount
    tmp_str = "Accuracy of all: {}".format(accuracy_all)
    print(tmp_str)
    discript += '\n' + tmp_str

    good_count = good_count1 + good_count2
    user_exp = good_count / test_amount
    tmp_str = "User experience: {}".format(user_exp)
    print(tmp_str)
    discript += '\n' + tmp_str

    ###################################################
    # Plot a figure
    ###################################################
    file_name = in_filename[:-9]
    out_file_text = out_address + file_name + '_bi_predict_with_partition.txt'
    with open(out_file_text, 'w') as output:
        output.write(discript)
    # out_file_png = out_address + file_name + '_bi_predict_with_error.png'
    # plt.savefig(out_file_png)

if __name__ == '__main__':
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen_tmp/'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    result_address_prefix = \
        '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_partition/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    for file in data_files:
        file_in = data_address_prefix + file
        print("in:", file_in)
        predict_bivar_judge_with_error(file_in, file, result_address_prefix)

