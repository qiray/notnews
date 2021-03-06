import re
import sys
from collections import defaultdict
from random import random

# Based on https://github.com/veekaybee/markovhn/blob/master/markov.py

lookback = 2

class Markov():

    def __init__(self, filename):
        self.filename = filename
        self.markov_map, self.titles = init(filename)

    def generate_sentence(self):
        sentence = []
        next_word = sample(self.markov_map[''].items())
        while next_word != '':
            sentence.append(next_word)
            next_word = sample(self.markov_map[' '.join(sentence[-lookback:])].items())
        sentence = ' '.join(sentence)
        for title in self.titles: #Prune titles that are substrings of actual titles
            if sentence in title:
                return self.generate_sentence()
        return sentence

    def get_sentences(self, count=10):
        sentences = []
        while len(sentences) < count:
            sentences.append(self.generate_sentence())
        for sentence in sentences:
            print (sentence)

def init(filename):
    archive = open(filename, encoding="utf-8")
    titles = archive.read().split("\n")
    archive.close()
    markov_map = defaultdict(lambda: defaultdict(int))
    
    #Generate map in the form word1 -> word2 -> occurences of word2 after word1
    for title in titles[:-1]:
        title = title.split()
        if len(title) > lookback:
            for i in range(len(title)+1):
                markov_map[' '.join(title[max(0,i-lookback):i])][' '.join(title[i:i+1])] += 1

    #Convert map to the word1 -> word2 -> probability of word2 after word1
    for _, following in markov_map.items():
        total = float(sum(following.values()))
        for key in following:
            following[key] /= total
    return markov_map, titles

#Typical sampling from a categorical distribution
def sample(items):
    next_word = None
    t = 0.0
    for k, v in items:
        t += v
        if t and random() < v/t:
            next_word = k
    return next_word
