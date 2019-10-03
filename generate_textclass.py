from text_stats import *
from itertools import accumulate
from collections import Counter
from random import uniform
from os import path
import sys
import itertools
import re
import numpy as np

class GenText:
    def __init__(self, filename):
        self.text = ""              # string, text file contents
        self.flag = False      		# boolean, text input flag
        self.sentences = []         # list(string), list of sentences
        self.sentancewords = []     # list(list(string)), nested list with words in sentances
        self.words = []             # list(string), list of words
        self.distinctwords = []     # list(tuple(string,int)), List of distinct words and corresponding frequencies
        self.total = 0        		# integer, total number of words
        self.numdistinctwords = 0   # integer, Number of distinct words in text
        self.nextwords = {}         # dict{string: dict{string: integer}},nested dictionary to be able to store following word and corresponding frequencies
        self.loadtext(filename)
		
    @staticmethod
    def transform2(text):
		# Removing punctuations
        text = re.sub(r"[\ufeff\u2014\n\t&/;,|]", " ", text)
        # Replace sentence terminators with period
        text = re.sub(r"[\]):?!]", ".", text)
        # Remove unwanted characters
        text = re.sub(r"[\u00C6\u00E6\u2018\u201C\u201D#0-9\[(`}\\_*\"]", "", text)
        # Remove trailing hyphens
        text = re.sub(r"(?=[a-zA-Z'-])-(?![a-zA-Z'])", "", text)
        #single space between words
        text = re.sub(r"[\s]+", " ", text)
		#converting text to lowercase for uniformity
        text = text.lower()
        return text
	
    def calcnextwords(self):
        # Create dictionary with distinct words as keys
        self.nextwords = {t[0]: {} for t in self.distinctwords}
        for sent in self.sentancewords:
            for i in range(0,len(sent)-1):
                word = sent[i]
                nextword = sent[i + 1]
                if nextword not in self.nextwords[word]:
                    self.nextwords[word][nextword] = 1
                else:
                    self.nextwords[word][nextword] += 1

    def calcwords(self):
	#sentances are split by period, words are extracted into a list and distinct words are found
        self.sentences = [sent.strip() for sent in self.text.split(".")]
        self.sentancewords = [sent.split(" ") for sent in self.sentences]
        self.words = [w for words in self.sentancewords for w in words]
        self.distinctwords = Counter(self.words).most_common()
        self.total = len(self.words)
        self.numdistinctwords = len(self.distinctwords)

    def loadtext(self, filename):
        if not path.exists(filename):
            print("The file does not exist!")
        elif not path.isfile(filename):
            print("Missing filename argument!")
        else:
            with open(filename, encoding="utf8") as file:
                self.text = file.read()
            self.flag = True

            # Clean text and create data structures
            self.text = self.transform2(self.text)
            self.calcwords()
            self.calcnextwords()

    @staticmethod
    def cumprobgen(obj, p):
        if len(obj) != len(p):
            raise ValueError("obj and probabilities dont match")

        unif = uniform(0, 1)
        cum_p = accumulate(p)  # Cumulative probabilities generator
        choice_ind = [i for i, cp in zip(range(len(obj)), cum_p) if unif <= cp][0]
        return obj[choice_ind]

    def nextwordgen(self, cur_word):
        # If unknown word is provided, next word cannot be generated
        if cur_word not in self.nextwords:
            return None
        nextword_options = list(self.nextwords[cur_word].keys())
        # if No following word after the current word
        if len(nextword_options) == 0:
            return None
        # Compute next word probabilities using word counts
        freq = self.nextwords[cur_word].values()
        freqsum = sum(freq)
        word_probs = [i / freqsum for i in freq]

        return self.cumprobgen(nextword_options, p=word_probs)

def generate_text(ts_obj, start_word, max_words):
    cur_word = start_word
    gen_words = [start_word]

    for i in range(max_words):
        nextword = ts_obj.nextwordgen(cur_word)
        if nextword:
            gen_words.append(nextword)
            cur_word = nextword
        else:
            break
    return " ".join(gen_words)


if __name__ == "__main__":
    file = sys.argv[1]
    gt = GenText(file)

#user defined arguments
file = sys.argv[1]
start_word = sys.argv[2]
max_word = int(sys.argv[3])

gentextobj = GenText(file)
#Output
if gentextobj.flag:
    generatedsentance = generate_text(gentextobj, start_word, max_word)
    print("{}".format(generatedsentance))

