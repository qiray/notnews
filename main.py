#!/bin/python3

import network
import zipfile

# TODOlist:
# TODO:
# get current date to download yesterday news
# use MarkovTextGenerator to parse downloaded news into database
# generate great news
# post it every hour
# clear old data and repeat on a new day

def main():
    filename = "news.zip"
    network.download_file("http://mediametrics.ru/data/archive/day/ru-2020-12-01.zip", filename)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("rawdata")

if __name__ == '__main__':
    main()