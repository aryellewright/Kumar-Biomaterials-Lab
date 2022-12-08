
with open('./20221105_N100H100_DSF.csv', 'r') as f:
    with open('./20221105_N100H100_DSF_new.csv', 'w+') as new_file:
        for i in f.readlines():
            new_line = i.split()
            new_line = ','.join(new_line)
            # print(new_line)
            new_file.write(new_line + '\n')