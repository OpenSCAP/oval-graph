import os
from glob import glob

path = os.getcwd()
pattern = os.path.join(path, "graph-of-*")
files = glob(pattern)
user_answer = None

if len(files):
    user_answer = input('Do you want delete %d files? [y/N]: ' % len(files))
else:
    print("Nothing to clean!")

if user_answer == 'y':
    for item in files:
        if not os.path.isdir(item):
            os.remove(item)
