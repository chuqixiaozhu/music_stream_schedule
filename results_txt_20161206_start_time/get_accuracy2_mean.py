import os

def get_accuracy2_mean():
    file_name = 'accuracy2.txt'
    with open(file_name) as fin:
        summary = 0
        count = 0
        count_max = 50
        for line in fin:
            id, acc = line.split()
            acc = float(acc)
            summary += acc
            count += 1
            if count == count_max:
                break

        mean = summary/count
        return mean

if __name__ == '__main__':
    mean = get_accuracy2_mean()
    print("2nd Accuracy mean:", mean)
