import os

# Use double backslashes (\\) on windows as path separator
DATAPATH = '/Users/nilsseitz/Downloads/dmdx_parse'

SUFFIX_DMDX = '.zil'  # dmdx file extension
INIT_TEXT = 'Subject'  # must be unique to lines that get text appended later
ADD_TEXT = ' COT'  # should contain a space before the actual word

if __name__ == '__main__':
    dmdx_filepaths = [os.path.join(root, file)  # all dmdx files for given path
                      for root, _, files in os.walk(os.path.dirname(DATAPATH))
                      for file in files if file.endswith(SUFFIX_DMDX)]

    for filepath in dmdx_filepaths:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        with open(filepath, 'w') as f:
            changed = 0
            for i, line in enumerate(lines):
                if line.startswith(INIT_TEXT):  # Check unique init condition
                    if not line.endswith(f'{ADD_TEXT}\n'):  # Check if preparsed
                        print(f'Changed line {i} in file location: {filepath}')
                        line = line.replace('\n', f'{ADD_TEXT}\n')
                        changed += 1
                f.write(line)
            print(f'Changed {changed} line{"s" if changed != 1 else ""} in '
                  f'file location: {filepath}')
