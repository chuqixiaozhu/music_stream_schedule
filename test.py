import numpy as np
from sklearn import mixture
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
#import cv2
import csv
import os
from get_marks import get_marks
from get_marks import is_same_interval
from table_of_confussion import get_table_of_confussion

def test():
    # marks = get_marks(10, 0, 0.1)
    # print('marks:', marks)#test

    A = [0, 0, 1, 1, 0]
    P = [0, 1, 0, 1, 1]
    table = get_table_of_confussion(A, P)
    print("table:", table)

    a = np.arange(15).reshape(5,3)
    b = a[2:,2]
    print(a)
    print(b)

    marks = get_marks(count=1, lower=0, upper=1)
    print('marks:', marks) #test
    a = 0.00000001
    b = 0.999999
    print("is_same_interval({}, {}): {}".format(\
        a, b, is_same_interval(a, b, marks)))

if __name__ == '__main__':
    test()