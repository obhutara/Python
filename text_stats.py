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

stop_words = stopwords.words('english')
#function that reads the file and prints an error message's for certain checks
def readfile():
	try:
		filename = sys.argv[1]
		if not os.path.isfile(filename):
			print("The file does not exist!") #*If the file does not exist, you need to print "The file does not exist!"
		with open(filename,"r",encoding="utf8") as file:
			data = file.read()
		return(data)
	
	#* If the user provides no such argument , an error message should be printed (not just an exception raised)
	except IndexError:
		print("Missing filename argument!")
	
	
#function that counts each letter in the text file 
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
	print('\n')
	print('Most frequenct words')
	wordsjoined = ' '.join(words)
	return(wordsjoined)
   
def frequencywords(words,n):
	outputstring = ""
	frequentwords = collections.Counter(words).most_common(5)
	for word,count in frequentwords:
		print(word,count)
		outputstring+= "\n{}({} times)".format(word,count)
	countflag = 1
	outputstring+= "\n"
	for word,count in frequentwords:
		nextcountflag = collections.Counter()
		for i,ind in enumerate(words):
			if ind == word:
				ind = words[i+1]
				nextcountflag[ind]+= 1
		print('\n')		
		print("\n{}({} times)".format(word,count))
		outputstring+= "\n{}({} times)".format(word,count)
		frequentwords2 = nextcountflag.most_common()
		for word2,count2 in frequentwords2[0:n]:
			print("->{}({} times)".format(word2,count2))
			outputstring+= "\n->{}({} times)".format(word2,count2)
		countflag = countflag+1 
		outputstring+= "\n"
	print(countflag)
	
	try:
		if len(sys.argv) > 1:
			with open(sys.argv[2],"w") as outputfile:
				outputfile.write(outputstring)
	except IndexError:
		print("No outputfile argument provided for contents to be written to")
	return(outputstring)
	#* If the user provides a second argument to the script, the
    #printout above should be written to that file as well.
		
def main():
	data = readfile()	
	frequencyletters(data)
	words = transform(data)
	words = removestopwords(words)
	distinctwords(words)
	frequencywords(words,n = 3)

	
if __name__ == '__main__':
	
	main()
	


# Question:
# In what way did you "clean up" or divide up the text into words (in the program; 
# the text files should be left unaffected)? This does not have to be perfect in any 
# sense, but it should at least avoid counting "lord",
 #"Lord" and "lord." as different words.




# Question: •	Which data structures have you used (such as lists, tuples, dictionaries, sets, ...)? Why does that
# choice make sense? You do not have to do any extensive research on the topics, or try to find exotic modern data
# structures, but you should reflect on which of the standard data types (or variants thereof) make sense. If you
# have tried some other solution and updated your code later on, feel free to discuss the effects!
  

