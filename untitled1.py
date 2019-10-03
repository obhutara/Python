import sys
import os.path
import nltk
import io
import itertools
import operator
import string
import re
import collections
from nltk.corpus import stopwords

stop_words=stopwords.words('english')

def readfile():
	try:
		filename=sys.argv[1]
		if not os.path.isfile(filename):
			print("This file does not exist")
		with open(filename,"r",encoding="utf8") as file:
			data = file.read()
		return(data)
	except IndexError:
		print("This file does not exist")
   
def frequencyletters(data):
    lettercount = collections.Counter(data.lower())
    for letter,count in lettercount.most_common():
        if letter in string.ascii_letters:
            print(letter,count)
    print('\n')

def transform(data): #function to clean and split the content of the text
	data = re.sub(r'[^\w\s]','',data)
	words = data.lower().split()
	print('Number of words in text file')
	print(len(words))
	print('\n')
	return(words)

def removestopwords(words): #function to remove commonly used conjunctions etc
	words = [w for w in words if w not in stop_words]
	return(words)
	
def distinctwords(words): #computes and prints count of unique words and also returns stopword removed string
	print('Count of distinct words')
	print(len(set(w.lower() for w in words)))
	print('Most frequenct words')
	wordsjoined = ' '.join(words)
	return(wordsjoined)
       
def frequentwords(words):
	frequentwords=collections.Counter(words).most_common(5)
	for word,count in frequentwords:
		print(word,count)
	countflag=1
	for word,count in frequentwords:
		nextcountflag = collections.Counter()
		for i,ind in enumerate(words):
			if ind == word:
				ind=words[i+1]
				nextcountflag[ind]+=1
		print('\n')
		print('\n')
		print("{}({} times)".format(word,count))
		frequentwords2=nextcountflag.most_common()
		for word2,count2 in frequentwords[0:5]:
			print("->{}({} times)".format(word2,count2))
		countflag= countflag+1 

def main():
	data=readfile()	
	frequencyletters(data)
	words=transform(data)
	words=removestopwords(words)
	distinctwords(words)
	frequentwords(words)
if __name__ == '__main__':
    main()
      