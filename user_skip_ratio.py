import os

def get_skip_ratio(file):
    with open(file) as fin:
        count = 0
        total = 0
        for line in fin:
            userid,lt,tt,percentage,artid,artist,traid,song = line.split('\t')
            # if float(percentage) >1:
            #     continue
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
    ratio_min = 1
    ratio_max = 0
    count = len(data_files)
    zero_count = 0
    one_count = 0
    i = 0
    i_max = 50
    
    with open('user_skip_ratio.txt', 'w') as fout:
        ratio_amount = 0
        for file in data_files:
            file_in = data_address_prefix + file
            ratio = get_skip_ratio(file_in)
            userid = file[5:11]
            fout.write(userid + ' ' + str(ratio) + '\n')
            if ratio == 1 or ratio == 0:
                count -= 1
                zero_count += 1 if ratio == 0 else 0
                one_count += 1 if ratio == 1 else 0
                continue
            ratio_amount += ratio
            if ratio > ratio_max:
                ratio_max = ratio
                ratio_max_id = userid
            if ratio < ratio_min:
                ratio_min = ratio
                ratio_min_id = userid
            i += 1
            if i == i_max:
                break
        ratio_mean = ratio_amount/i
        print("mean ratio:", ratio_mean)
        print("ratio min:", ratio_min, "userID:", ratio_min_id)
        print("ratio max:", ratio_max, "userID:", ratio_max_id)
        print("zero count:", zero_count)
        print("one count:", one_count)
