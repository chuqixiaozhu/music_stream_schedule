import os

def get_record_num(file_in):
    with open(file_in) as fin:
        lines = fin.readlines()
        return len(lines)

if __name__ == '__main__':
    data_address_prefix = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    data_files = os.listdir(data_address_prefix)
    data_files.sort()
    with open('user_record_num.txt', 'w') as fout:
        record_amount = 0
        for file in data_files:
            file_in = data_address_prefix + file
            count = get_record_num(file_in)
            userid = file[5:11]
            fout.write(userid + ' ' + str(count) + '\n')
            record_amount += count
        record_mean = record_amount/len(data_files)
        print("mean number:", record_mean)