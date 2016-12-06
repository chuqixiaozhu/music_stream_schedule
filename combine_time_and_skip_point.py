import os

def combile_two_files(time_file, skip_point_file, user_id):
    combiled_file = '/scratch/zpeng.scratch/pppp/music/data/time_and_skip/' \
                    + user_id + '_com.tsv'
    with open(time_file) as t_input, \
        open(skip_point_file) as s_input, \
        open(combiled_file, 'w') as c_output:
        t_lines = t_input.readlines()
        s_lines = s_input.readlines()
        j = 0
        for i in range(len(s_lines)):
            s_line = s_lines[i]
            s_words = s_line.split('\t')
            is_found = False
            while j < len(t_lines) and not is_found:
                t_line = t_lines[j]
                t_words = t_line.split('\t')
                if s_words[4] == t_words[2] \
                    and s_words[6] == t_words[4]:
                    c_words = t_words[:2] + s_words[1:]
                    c_line = '\t'.join(c_words)
                    c_output.write(c_line)
                    is_found = True
                j += 1

        # for i in range(len(t_lines)):
        #     t_line = t_lines[i]
        #     s_line = s_lines[i]
        #     t_words = t_line.split('\t')
        #     s_words = s_line.split('\t')

        # for t_line, s_line in zip(t_input, s_input):
        #     t_words = t_line.split('\t')
        #     s_words = s_line.split('\t')
        #     c_words = t_words[:2]
        #     c_words.extend(s_words[1:])
        #     c_line = '\t'.join(c_words)
        #     c_output.write(c_line + '\n')



def get_combine():
    """ When I get the skip point of user and write it into a new tsv file,
    I stupidly dropped the time record of original record. Because of this,
    we cannot use the time of listening start as the input of regressor.
    Now I have to add the original time record into the skip point record
    file, and feed the combined record into the regressor to hopefully get
    a better prediction result."""

    # Read records from two files
    time_file_address = '/scratch/zpeng.scratch/pppp/music/data/backup/'
    skip_point_file_address = '/scratch/zpeng.scratch/pppp/music/data/listen/'
    time_files = os.listdir(time_file_address)
    time_files.sort()
    skp_files = os.listdir(skip_point_file_address)
    skp_files.sort()

    count = len(time_files) \
            if len(time_files) < len(skp_files) \
            else len(skp_files)
    for i in range(count):
        t_file = time_files[i]
        user_id = t_file[:-4]
        s_file = skp_files[i]
        t_file = time_file_address + t_file
        s_file = skip_point_file_address + s_file
        combile_two_files(t_file, s_file, user_id)




    # Combine the single record

    # Write the record to a new file

if __name__ == '__main__':
    get_combine()