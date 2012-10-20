import nltk
import os
import pandas as pd

def tokenize_sentence(sentence,unique_stop_words=[]):
	'''REQUIRES: a sentence
	unique_stop_words is a list of additional stop words you define e.g. ['wall','street']
	RETURNS: a list of tokens split by spaces without stop words
	'''

	words = []

	for word in sentence.split(' '):
		stopwords = nltk.corpus.stopwords.words('english')
		stopwords = stopwords + unique_stop_words 
		if not word.lower() in stopwords:
			words.append(word.lower())

	return words

def tokenize_text_list(text_list,unique_stop_words=[]):
#REQUIRES: text_list is a list of sentences; unique_stop_words is a list of additional stopwords you can define
#RETURNS: a list of tokens without stop words
    words = []
    for text in text_list:
        text = text.strip()
        #words = [word.lower() for word in text.split(' ') if not word.lower() in nltk.corpus.stopwords.words('english')]
        for word in text.split(' '):
            stopwords = nltk.corpus.stopwords.words('english')
            stopwords = stopwords + unique_stop_words 
            if not word.lower() in stopwords:
                words.append(word.lower())
    return words

def print_top_words(fb_text,limit = 50):
#REQUIRES: a list of tokens
#PRINTS THE TOP limit Words
    fdist = nltk.FreqDist(word_tokenize(fb_text))
    papername = posts_df['name'][0]
    print "%s has %s unique words" % (papername, str(len(fdist.keys())))
    fig = plt.figure(figsize = (10,6),dpi = 50)
    ax = fig.add_subplot(111)
    ax.set_title("Top %s Words for %s" % (limit,papername))
    fdist.plot(limit,cumulative = True)

def document_features(document):

	words_list = word_tokenize(sentence)
	#for word in words_list:
	#	features[word] = 

def build_feature_set(filepath,delim = '\t'):
	''' REQUIRES: filepath that contains training data
	delim is optional parameter, default = \t
	RETURNS: dictionary of features
	'''
	
	documents = []

	if(os.path.isfile(filepath)):
		with open(filepath,'r') as f:
			for line in f:
				sentiment, sentence = line.strip().split(delim)
				documents.append((tokenize_sentence(sentence),sentiment)) 
	
	#features = {}
	return documents

filepath = "training.txt"
