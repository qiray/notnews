#!/bin/python3

import datetime
import network
import os
import sys
import shutil
import zipfile

from getch import getch
from markov import get_sentences

OUTFILE = "data.txt"

# TODOlist:
# TODO:
# https://github.com/minimaxir/textgenrnn
# use markov.py to parse text to database (USE -n 1 only)
# Get data from panorama.pub?
# Use https://github.com/veekaybee/markovhn.git or https://gist.github.com/grantslatton/7694811
# Find and fix typos (https://github.com/intgr/topy), punctuation errors and grammatical errors (https://pypi.org/project/grammar-check/). Maybe not needed.
# Fix quotes errors
# generate great news
# post it every hour
# clear old data and repeat on a new day
# copyrights
# new mode: generate one news and wait for user decision: if "+" -> move news to whitelist. Later publish news from whitelist.

def unique(filename):
    uniqlines = set(open(filename, encoding="utf-8").readlines())
    open(filename, 'w', encoding="utf-8").writelines(uniqlines)

def parse_files(dirname):
    files = os.listdir(dirname)
    outfile = open(OUTFILE, 'w', encoding="utf-8")
    nonBreakSpace = u'\xa0'
    for filename in files:
        with open(dirname + "/" + filename, encoding="utf-8") as f:
            next(f)
            for line in f:
                data = line.split("\t")
                value = data[1].replace("&quot;", "\"").replace(nonBreakSpace, " ")
                outfile.write(value + "\n")
    outfile.close()
    unique(OUTFILE)

def main(argv):
    update_data = False
    generate_sentences = False
    if len(argv) < 2:
        print("No params specified. Using default values.")
        argv.extend(("-u", "-g"))
    args_dict = { i : True for i in argv }
    if "-u" in args_dict:
        update_data = True
    if "-g" in args_dict:
        generate_sentences = True
    if "-h" in args_dict:
        print("Help info") # TODO: print help info
        return
    if "-a" in args_dict:
        print("About info") # TODO: print about info
        return
    if "-i" in args_dict:
        user_input = getch()
        print(user_input)
    # TODO: new mode: generate one news and wait for user decision: if "+" -> move news to whitelist. Later publish news from whitelist.
    if update_data:
        dirname = "rawdata"
        shutil.rmtree(dirname, ignore_errors=True)
        filename = "news.zip"
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        network.download_file("http://mediametrics.ru/data/archive/day/ru-{}.zip".format(yesterday), filename)
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(dirname)
        parse_files(dirname + "/day")
    
    if generate_sentences:
        get_sentences(OUTFILE)

if __name__ == '__main__':
    main(sys.argv)
