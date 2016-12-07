import os

def get_skip_ratio(file):
    with open(file) as fin:
        count = 0
        total = 0
        for line in fin:
            userid,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
            if float(percentage) >1:
                continue
            total += 1
            if float(percentage) < 1:
                count += 1
        if total == 0:
            result = 0
        else:
            result = count/total
        return result

if __name__ == '__main__':
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    with open('user_skip_ratio.txt', 'w') as fout:
        ratio_amount = 0
        for file in data_files:
            file_in = data_address_prefix + file
            ratio = get_skip_ratio(file_in)
            userid = file[5:11]
            fout.write(userid + ' ' + str(ratio) + '\n')
            ratio_amount += ratio
        ratio_mean = ratio_amount/len(data_files)
        print("mean ratio:", ratio_mean)
