import os

def get_record_num(file_in):
    with open(file_in) as fin:
        lines = fin.readlines()
        return len(lines)

if __name__ == '__main__':
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    record_min = 2000
    record_max = 0
    count = 0
    count_max = 50

    with open('user_record_num.txt', 'w') as fout:
        record_amount = 0
        for file in data_files:
            file_in = data_address_prefix + file
            num = get_record_num(file_in)
            userid = file[5:11]
            fout.write(userid + ' ' + str(num) + '\n')
            record_amount += num
            if num > record_max:
                record_max = num
                record_max_id = userid
            if num < record_min:
                record_min = num
                record_min_id = userid
            count += 1
            if count == count_max:
                break
        record_mean = record_amount/count
        print("mean number:", record_mean)
        print("number min:", record_min, "userID:", record_min_id)
        print("number max:", record_max, "userID:", record_max_id)