#!/bin/python3

import datetime
import network
import os
import sys
import shutil
import zipfile

from markov import get_sentences

# sys.path.append('MarkovTextGenerator')

OUTFILE = "data.txt"

# TODOlist:
# TODO:
# https://github.com/minimaxir/textgenrnn
# use markov.py to parse text to database (USE -n 1 only)
# Use https://github.com/veekaybee/markovhn.git or https://gist.github.com/grantslatton/7694811
# Find and fix typos (https://github.com/intgr/topy), punctuation errors and grammatical errors (https://pypi.org/project/grammar-check/). Maybe not needed.
# Fix quotes errors
# generate great news
# post it every hour
# clear old data and repeat on a new day

def unique(filename):
    uniqlines = set(open(filename, encoding="utf-8").readlines())
    open(filename, 'w', encoding="utf-8").writelines(uniqlines)

def parse_files(dirname):
    files = os.listdir(dirname)
    outfile = open(OUTFILE, 'w', encoding="utf-8") 
    for filename in files:
        with open(dirname + "/" + filename, encoding="utf-8") as f:
            next(f)
            for line in f:
                data = line.split("\t")
                value = data[1].replace("&quot;", "\"")
                outfile.write(value + "\n")
    outfile.close()
    unique(OUTFILE)

def main():
    dirname = "rawdata"
    # shutil.rmtree(dirname, ignore_errors=True)
    filename = "news.zip"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    network.download_file("http://mediametrics.ru/data/archive/day/ru-{}.zip".format(yesterday), filename)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(dirname)
    parse_files(dirname + "/day")

if __name__ == '__main__':
    main()
    get_sentences(OUTFILE)
