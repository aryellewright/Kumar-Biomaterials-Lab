"""
This function will reformat a csv that has space delimiter instead of comma.

:params:[Required] filename: Name of csv file to be read in
:params:[Optional] new_file_postfix: Postfix of new file to not have duplicate.
                                     default='_new'
"""


def remove_spaces(filename: str, new_file_postfix: str = '_new'):
    with open(filename, 'r') as f:
        new_filename = filename.split('.')
        new_filename = f'{new_filename[0]}{new_file_postfix}.csv'
        with open(new_filename, 'w+') as new_file:
            for i, row in enumerate(f.readlines()):
                new_line = row.split()
                if i != 0:
                    new_line = new_line[:2] + new_line[3:]

                new_line = ','.join(new_line)
                new_file.write(new_line + '\n')


remove_spaces('20221104_N100H100N75H25N50H50N25H75.csv')
remove_spaces('20221105_N100H100_DSF.csv')
