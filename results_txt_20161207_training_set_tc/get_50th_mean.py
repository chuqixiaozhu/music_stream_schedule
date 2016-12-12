import os
import sys

count_max = 50

def get_50th_mean(file_name):
    with open(file_name) as fin:
        count = 0
        amount = 0
        for line in fin:
            id, num = line.split()
            num = float(num)
            amount += num
            count += 1
            if count == count_max:
                break
        mean = amount/count
        return mean
            

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("Error: no destinated file")
        exit()
        
    result = get_50th_mean(file_name)
    print("Mean of first 50 records of {}: {}".format(sys.argv[1], result))