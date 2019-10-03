from text_stats import *
import random
import collections
import sys
import itertools
import re
import numpy as np

def generatetext(text,start_word,max_word):
	cur_word = start_word
	n = int(max_word)
	msg = cur_word
	data = readfile()
	words = transform(data)
	words = removestopwords(words)
	nextcount = collections.Counter()
	probweight = []
	selectedwords = []
	frequency = 0
	msglength = 1
	for i,ind in enumerate(words):
		if ind == cur_word:
			frequency = frequency+1
			ind = words[i]
			nextcount[ind]+= 1
	nextword = nextcount.most_common()
	sum_list = []
	prob = 0
	for i in range(len(nextword)):
		prob = prob+nextword[i][1]/frequency
		sum_list.append(prob)
	probweight = prob*random.random()
	cur_word = nextword[i][0]
	msg = msg+" "+cur_word
	msglength = msglength+1
	while nextword[0][1] > 0 and msglength <= n:
		sum_list = []
		prob = 0
		nextcount = collections.Counter()
		for i,j in enumerate(words):
			if j == cur_word:
				j = words[i+1]
				nextcount[j]+= 1
		nextword = nextcount.most_common()
		for i in range(len(nextword)):
			prob+= nextword[i][1]/frequency
			sum_list.append(prob)
		probweight = prob*random.random()		
		for i, j in enumerate(sum_list):
			if probweight < j:
			   break
		cur_word = nextword[i][0]
		msg+= " " + cur_word
		msglength = msglength+1
	print(msg)
	
def wordcollectioncounter(words, p = True):
	count = collections.Counter()
	wordfreq = []
	for i,ind in enumerate(words):
		ind = words[i]
		count[ind]+= 1
		[wordfreq.append(count[ind])]
	wordfreq = list(zip(words, wordfreq))
	wordfreq = list(set(wordfreq))
	wordfreq = sorted(wordfreq, key = lambda x: (-x[1], x[0]))
	return wordfreq
	
def generatetext2(text,start_word,max_word):
	cur_word = start_word
	n = int(max_word)
	msg = cur_word
	max_wordcount = 0
	while max_wordcount <= max_word:
		nextwordindex = [i+1 for i,j in enumerate(text) if j==cur_word]
		nextword = ([text[i] for i in nextwordindex])
		#p is boolean to print or not
		nextwordncount = (wordcollectioncounter(nextword, p = False))
		#break if no nextword 
		if len(nextwordindex) == 0:
			break
		freq = [i[1] for i in nextwordncount]
		#word frequency is accessed and cumulative sum of the word frequencies
		freqsum = sum(freq)
		#probability
		pr = [i/freqsum for i in freq]	
		#weighted by how likely cur_word is to be succeeded by it
		randweightedsuccessor = (np.random.choice(np.arange(len(freq)), p=pr))
		cur_word = (nextwordncount[randweightedsuccessor][0])
		msg += " " + cur_word
		#msg += " ".join({}).format(cur_word)
		max_wordcount += 1
		#joint += '  " ".join({})\n'.format(("NaNaNaNa "*N).split())
	print(msg)
	return msg

def main():
	data = readfile()
	words = transform(data)
	words = removestopwords(words)
	generatetext2(words,sys.argv[2],int(sys.argv[3]))
	
if __name__ == '__main__':
	main()	