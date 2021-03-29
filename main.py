#!/bin/python3

import datetime
import network
import os
import sys
import shutil
import zipfile

from getch import getch
from markov import Markov

OUTFILE = "data.txt"
GOODFILE = "good.txt"

APP_NAME = "NotNews"
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

# TODOlist:
# TODO:
# Get data from panorama.pub?
# generate great news
# post it every hour (twitter, telegram, vk)
# clear old data and repeat on a new day
# add copyrights

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

def get_version():
    return "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_about_info():
    return ("\n" + APP_NAME + " " + get_version() + " Copyright (C) 2020-2021 Yaroslav Zotov.\n" +
        "This program comes with ABSOLUTELY NO WARRANTY.\n" +
        "This is free software under MIT license; see the LICENSE file for copying conditions.\n")

def main(argv):
    update_data = False
    generate_sentences = False
    interactive_mode = False
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
        print(get_about_info())
        return
    if "-i" in args_dict:
        interactive_mode = True
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
        markov = Markov(OUTFILE)
        markov.get_sentences()
    
    if interactive_mode:
        markov = Markov(OUTFILE)
        outfile = open(GOODFILE, 'a', encoding="utf-8") # TODO: post these news
        while True:
            sentence = markov.generate_sentence()
            print(sentence)
            user_input = getch()
            if user_input == "\x1b":
                break
            elif user_input == "+":
                outfile.write(sentence + "\n")
                pass
        outfile.close()

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        exit()
    except EOFError:
        exit()
