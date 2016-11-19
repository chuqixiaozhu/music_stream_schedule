import numpy as np
from sklearn import mixture
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
#import cv2
import csv
import os

def predict_bivar_judge_with_error(in_file, in_filename, out_address):
    # load data
    #with open('G:\\vs2010\\test set and training set\\user_000002_time.tsv','rU') as tsvin, open('G:\\vs2010\\test set and training set\\test.csv','wb') as csvout:
    #    tsvin = csv.reader(tsvin,delimiter = '\t')
    #    csvout = csv.writer(csvout,delimiter = '\t')
    #    for row in tsvin:
    #        count = row[3]
    #        try:
    #            float(count)
    #            if float(count) <= 1 and float(count) > 0:
    #                data = [row[5]+','+row[7]+','+row[3]]
    #                csvout.writerows(data)
    #        except ValueError:
    #            print "Not a float"

    # tansfer string to number so that we can train
    data = []
    # with open('/scratch/zpeng.scratch/pppp/music/data/listen/user_000002_time.tsv') as f:
    with open(in_file, 'r') as f:
        for line in f:
            # song,l,artist,percentage,a4,a5,a6 = line.split(",")
            userid,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
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

            data.append([float(px),float(py),percentage])

    #np.save('G:/vs2010/test set and training set/feature2', data)


    #training two randomforestregressor models, one for judge whether it is 1 or 0, the other is used to judge the specific number less than zero
    data = np.asarray(data,dtype='float')
    #gmm1 = mixture.GaussianMixture(n_components=7,covariance_type='full')
    estimator = RandomForestRegressor(n_estimators = 100)

    not_one_index = np.where(data[:,2]!=1)[0]
    zero_y = data.copy()
    zero_y[not_one_index,2] = 0
    #gmm1.fit(data[:,:2],y = zero_y[:,2])
    #training phase
    train_start = 0
    # train_end = 22000
    train_end = int(np.floor(data.shape[0] * 2/3))
    estimator.fit(data[train_start:train_end,:2],y = zero_y[train_start:train_end,2])

    #training another model to find the exact number
    #gmm2 = mixture.GaussianMixture(n_components=5,covariance_type='full')
    estimator2 = RandomForestRegressor(n_estimators = 100)
    #gmm2.fit(data[:,:2],y = data[:,2])
    estimator2.fit(data[train_start:train_end,:2],y = data[train_start:train_end,2])
    #predicting
    #result2 = gmm2.predict(data[300:400,:2])

    #predicting phase
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
    result[none_zero_index] = 1
    result[zero_index] = 0
    #calculate the precision
    counter = 0
    i = 0
    for item in result:
        if item==zero_y[i+test_start,2]:
            counter += 1
        i+=1

    print ("precision of 0-1 judge: {0:.0f}%".format(float(counter)/len(test_index)*100))
    discript = "precision of 0-1 judge: {0:.0f}%".format(float(counter)/len(test_index)*100)

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
    result2 = result2.astype(float)
    # error = result2-data[index,2]
    error = abs(result2-data[index,2])
    mse = sum(error**2) / len(error)

    test_count = len(error)
    error_mean = np.mean(error)
    right_count = 0
    for delta in error:
        # if abs(delta) <= error_mean/2:
        if abs(delta) <= error_mean:
        # if abs(delta) <= mse:
            right_count += 1
    ratio_predict = right_count / test_count
    print("Number of test: {}".format(test_count))
    discript += "\nNumber of test: {}".format(test_count)
    print("Precision of skip judge: {:f}%".format(ratio_predict * 100))
    discript += "\nPrecision of skip judge: {:f}%".format(ratio_predict * 100)

    print ("mean of error: {}".format(np.mean(error)))
    discript += "\nmean of error: {}".format(np.mean(error))
    print ("max of error: {}".format(error.max()))
    discript += "\nmax of error: {}".format(error.max())
    print ("min of error: {}".format(error.min()))
    discript += "\nmin of error: {}".format(error.min())

    n,bins,patches = plt.hist(error,20,facecolor='green',alpha=0.5)
    plt.xlabel('error')
    plt.ylabel('number')
    plt.title(r'Histogram of prediction error')

    # plt.show()
    file_name = in_filename[:-9]
    out_file_text = out_address + file_name + '_bi_predict_with_error.txt'
    out_file_png = out_address + file_name + '_bi_predict_with_error.png'
    with open(out_file_text, 'w') as output:
        output.write(discript)
    plt.savefig(out_file_png)

if __name__ == '__main__':
    # data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen_tmp/'
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    result_address_prefix = \
        '/scratch/zpeng.scratch/pppp/music/data/predict_bi_with_error/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    for file in data_files:
        file_in = data_address_prefix + file
        print("in:", file_in)
        predict_bivar_judge_with_error(file_in, file, result_address_prefix)