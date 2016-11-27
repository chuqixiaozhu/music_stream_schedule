import numpy as np
from sklearn import mixture
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
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
    track_time_all = []
    # with open('/scratch/zpeng.scratch/pppp/music/data/listen/user_000002_time.tsv') as f:
    with open(in_file, 'r') as f:
        for line in f:
            # song,l,artist,percentage,a4,a5,a6 = line.split(",")
            userid,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
            track_time_all.append(float(tt)/1000)
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
    #gmm1 = mixture.GaussianMixture(n_components=7,covariance_type='full')
    estimator = RandomForestRegressor(n_estimators = 100)

    not_one_index = np.where(data[:,2]!=1)[0]
    zero_y = data.copy()
    zero_y[not_one_index,2] = 0 # 0 means Skip
    #gmm1.fit(data[:,:2],y = zero_y[:,2])
    #training phase
    train_start = 0
    # train_end = 22000
    train_end = int(np.floor(data.shape[0] * 2/3))
    estimator.fit(data[train_start:train_end,:2],y = zero_y[train_start:train_end,2])

    #predicting
    #result2 = gmm2.predict(data[300:400,:2])

    ###################################################
    # 1st Predicting phase
    ###################################################
    #result = gmm1.predict(data[300:400,:2])
    # test_start = 22000
    test_start = train_end
    test_end = data.shape[0]
    # test_index = [t for t in xrange(test_start,test_end)]
    test_index = [t for t in range(test_start,test_end)]
    try:
        result = estimator.predict(data[test_index,:2])
    except:
        print("Exception: the 1st prediction failed.")
        return
    result = result.astype(float)
    none_zero_index = np.where(result>=0.5)
    zero_index = np.where(result<0.5)
    result[none_zero_index] = 1 # 1 means Non-Skip
    result[zero_index] = 0 # 0 means Skip
    ###################################################
    # Calculate the precision for 1st judgement
    ###################################################
    counter = 0
    i = 0
    for item in result:
        if item==zero_y[i+test_start,2]:
            counter += 1
        i+=1
    # tmp_str = "precision of 0-1 judge: {0:.1f}%".format(float(counter)/len(test_index)*100)
    # print(tmp_str)
    # discript = tmp_str

    A = zero_y[test_start:,2]
    P = result
    tc = get_table_of_confussion(A, P)
    tp = tc['TP'] # True Positive 
    tn = tc['TN'] # True Negative
    fp = tc['FP'] # False Positive
    fn = tc['FN'] # False Negative
    accuracy = (tp + tn) / len(P)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2*tp / (2*tp + fp + fn)
    tmp_str = '0-1 Judge: Accuracy: ' + str(accuracy) + '\n' + \
                'Precision: ' + str(precision) + '\n' + \
                'Recall: ' + str(recall) + '\n' + \
                'F1 Score: ' + str(f1_score)
    print(tmp_str)
    discript = tmp_str

    ###################################################
    # Predict skip point
    ###################################################
    one_index = np.where(data[:,2] >= 1)[0]
    data[one_index,2] = 1 # 1 means Non-Skip
    marks = get_marks(count=10, lower=0, upper=1)
    for i in range(data.shape[0]):
        sp = data[i,2]
        label = get_label(sp, marks)
        data[i,2] = int(label)

    #training another model to find the exact number
    #gmm2 = mixture.GaussianMixture(n_components=5,covariance_type='full')
    # estimator2 = RandomForestRegressor(n_estimators = 100)
    estimator2 = RandomForestClassifier(n_estimators = 100)
    #gmm2.fit(data[:,:2],y = data[:,2])
    estimator2.fit(data[train_start:train_end,:2],y = data[train_start:train_end,2])

    index = np.copy(test_index)
    index = list(index)
    for t in none_zero_index[0]:
        tt = t+test_start
        index.remove(tt)
    try:
        result2 = estimator2.predict(data[index,:2])
    except:
        print("Exception: the 2nd prediction failed.")
        return
    # result2 = result2.astype(float) # !!!!!!!!!!!!!!!!!!!!!!!
    # error = abs(result2-data[index,2])

    ###################################################
    # Calculate 2nd Predict Accuracy
    ###################################################
    A = data[index,2]
    P = result2
    test_amount = len(P)
    true_count = 0
    # marks = get_marks(count=10, lower=0, upper=1)
    for i in range(test_amount):
        act = A[i]
        pre = P[i]
        # if is_same_interval(act, pre, marks):
        if act == pre:
            true_count += 1
    accuracy = true_count / test_amount
    tmp_str = "Precision of skip judge: {}%".format(accuracy * 100)
    print(tmp_str)
    discript += '\n' + tmp_str

    good_count = 0
    for i in range(test_amount):
        act = A[i]
        pre = P[i]
        if pre >= act:
            good_count += 1
    user_exp = good_count / test_amount
    tmp_str = "User experience: {}%".format(user_exp * 100)
    print(tmp_str)
    discript += '\n' +tmp_str

    # test_count = len(error)
    # error_mean = np.mean(error)
    # # error_threshold = error_mean
    # error_threshold = error_mean/2
    # right_count = 0
    # for delta in error:
    #     if abs(delta) <= error_threshold:
    #         right_count += 1
    # ratio_predict = right_count / test_count
    # tmp_str = "Number of test: {}".format(test_count)
    # print(tmp_str)
    # discript += '\n' + tmp_str
    # tmp_str = "Precision of skip judge: {:.1f}%".format(ratio_predict * 100)
    # print(tmp_str)
    # discript += '\n' + tmp_str
    # track_time_test_all = []
    # for i in index:
    #     track_time_test_all.append(track_time_all[i])
    # track_time_mean = np.mean(track_time_test_all)
    # ratio_error2tracktime = error_threshold / track_time_mean
    # tmp_str = \
    #     "Ratio of mean error to mean track time: {:.1f}%".format(ratio_error2tracktime*100)
    # print(tmp_str)
    # discript += '\n' + tmp_str
    # tmp_str = "mean of error: {}".format(np.mean(error))
    # print(tmp_str)
    # discript += '\n' + tmp_str
    # tmp_str = "max of error: {}".format(error.max())
    # print(tmp_str)
    # discript += '\n' + tmp_str
    # tmp_str = "min of error: {}".format(error.min())
    # print(tmp_str)
    # discript += '\n' + tmp_str

    ###################################################
    # Plot a figure
    ###################################################
    # n,bins,patches = plt.hist(error,20,facecolor='green',alpha=0.5)
    # plt.xlabel('error')
    # plt.ylabel('number')
    # plt.title(r'Histogram of prediction error')
    # plt.show()

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

