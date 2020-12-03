#!/bin/python3

import datetime
import network
import os
import shutil
import zipfile

OUTFILE = "data.txt"

# TODOlist:
# TODO:
# use MarkovTextGenerator to parse text to database (USE -n 1 only)
# generate great news
# post it every hour
# clear old data and repeat on a new day

def unique(filename):
    uniqlines = set(open(filename).readlines())
    out = open(filename, 'w').writelines(uniqlines)

def parse_files(dirname):
    files = os.listdir(dirname)
    outfile = open(OUTFILE, 'w') 
    for filename in files:
        with open(dirname + "/" + filename) as f:
            next(f)
            for line in f:
                data = line.split("\t")
                value = data[1].replace("&quot;", "\"")
                outfile.write(value + ".\n")
    outfile.close()
    unique(OUTFILE)

def main():
    dirname = "rawdata"
    # shutil.rmtree(dirname, ignore_errors=True)
    try:
        os.remove("data.db")
    except OSError:
        pass
    filename = "news.zip"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    network.download_file("http://mediametrics.ru/data/archive/day/ru-{}.zip".format(yesterday), filename)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(dirname)
    parse_files(dirname + "/day")

if __name__ == '__main__':
    main()