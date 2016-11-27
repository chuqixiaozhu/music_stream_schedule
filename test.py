import numpy as np
from sklearn import mixture
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
#import cv2
import csv
import os
from get_marks import get_marks
from get_marks import is_same_interval
from get_marks import get_label
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

    marks = get_marks(count=10, lower=0, upper=1)
    print('marks:', marks) #test
    a = 0.00000001
    b = 0.999999
    print("is_same_interval({}, {}): {}".format(\
        a, b, is_same_interval(a, b, marks)))
    for i in range(10):
        pass
    print("i:", i)
    val = 0.9999
    label = get_label(val, marks)
    print("label:", label)
    a = (3,5)
    print("a[0]:", a[0])
    a = np.arange(6).reshape(3,2)
    b = a.shape[0]
    print("b:", b)
    a = 1
    print("a:", a)
    a = 6.0
    b = 6
    print("a == b :", a == b)

if __name__ == '__main__':
    test()