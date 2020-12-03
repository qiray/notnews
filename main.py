#!/bin/python3

import network
import zipfile
import shutil
import datetime

# TODOlist:
# TODO:
# parse downloaded news into text
# use MarkovTextGenerator to parse text to database
# generate great news
# post it every hour
# clear old data and repeat on a new day

def main():
    dirname = "rawdata"
    shutil.rmtree(dirname, ignore_errors=True)
    filename = "news.zip"
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    network.download_file("http://mediametrics.ru/data/archive/day/ru-{}.zip".format(yesterday), filename)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(dirname)

if __name__ == '__main__':
    main()
