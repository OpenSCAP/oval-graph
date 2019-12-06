import fileinput
import re
import os
from glob import glob
from shutil import rmtree

"""
cleandir is function which removes generated reports.
"""


def cleandir():
    path = os.getcwd()
    pattern = os.path.join(path, "graph-of-*")

    for item in glob(pattern):
        if not os.path.isdir(item):
            continue
        rmtree(item)


"""
Data_cleaner is script which removes randomly generated items from test files.
"""


def replace_hash(line):
    return re.sub(
        r'([a-zA-Z]|\d){8}-([a-zA-Z]|\d){4}-([a-zA-Z]|\d){4}-([a-zA-Z]|\d){4}-([a-zA-Z]|\d){12}',
        'UUID-HASH',
        str(line))


path = './'

files = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file_ in f:
        if '.json' in file_ or '.js' in file_:
            files.append(os.path.join(r, file_))

for file_src in files:
    print(file_src)
    with fileinput.FileInput(file_src, inplace=True) as f:
        for line in f:
            print(replace_hash(line), end="")
