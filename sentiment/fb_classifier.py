from my_tokenizers import *
import nltk
import os
import pandas as pd


def print_top_words(fb_text,limit = 50):
#REQUIRES: a list of tokens
#PRINTS THE TOP limit Words
    fdist = nltk.FreqDist(tokenize_text_list(fb_text))
    papername = posts_df['name'][0]
    print "%s has %s unique words" % (papername, str(len(fdist.keys())))
    fig = plt.figure(figsize = (10,6),dpi = 50)
    ax = fig.add_subplot(111)
    ax.set_title("Top %s Words for %s" % (limit,papername))
    fdist.plot(limit,cumulative = True)

def get_word_features_set(filepath,tokenizer_func=tokenize_sentence_emote,delim = '\t'):
	''' REQUIRES: filepath that contains training data
	delim is optional parameter, default = \t
	RETURNS: set of unique words in training data; this will be the word features
	for your training set
	'''
	
	word_list = []

	if(os.path.isfile(filepath)):
		with open(filepath,'r') as f:
			for line in f:
				sentiment, sentence = line.strip().split(delim)
				for token in tokenizer_func(sentence):
					word_list.append(token)

	word_distribution = nltk.FreqDist(word_list)

	#use the top 20000 most frequent words for our training data
	vocabulary = word_distribution.keys()[:20000]

	return vocabulary

filepath = "training.txt"
vocabulary = get_word_features_set(filepath)
def extract_feature_presence(document):
	'''REQUIRES: set of vocabulary words and tokenized document list 
	RETURNS: dictionary of words and whether or not it's present
	{'cat': false
	 'dog': true
	 ...}
	 '''

	#getting all unique words from each document
	#this extracts word features for a binomial classifier
	#document_words = tokenize_sentence_emote(document) 
	document_words = set(document)


	word_features = {}
	
	count = 0
	for word in vocabulary:
		try:
			word_features[word] = (word in document_words)
		except:
			print "this is word", word
			print "this is document", document
			count += 1

	print "Errors is ", count
	return word_features

def get_nltk_training_set(filepath,tokenizer_func = tokenize_sentence_emote,delim = '\t'):

	labeled_document_list = []

	if(os.path.isfile(filepath)):
		with open(filepath,'r') as f:
			for line in f:
				sentiment, sentence = line.strip().split(delim)
				temp = (tokenizer_func(sentence),sentiment)
				labeled_document_list.append(temp)
	
	training_set = nltk.classify.apply_features(extract_feature_presence,labeled_document_list)
	return training_set			


def store_model(filepath, data):
	'''REQUIRES: filepath and data
	PURPOSE: allows me to save my models for later usage
	'''
	import pickle
	f = open(filepath,'wb')
	pickle.dump(classifier,f)
	f.close()

def load_model(filepath):
	import pickle
	f = open(filepath);
	model = pickle.load(f)
	f.close()
	return(model)


def train_classifier(filepath = "training.txt"):
#sample code to show how to run the classifier

	import time
	start = time.clock()

	vocabulary = get_word_features_set(filepath)
	training_set = get_nltk_training_set(filepath)
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	elapsed = (time.clock()-start)

	print "Classifier training time is %s s " % elapsed
	label = classifier.classify(extract_feature_presence("this is a test.. !!!"))
	
	if(label == 1):
		print "Sentence is classified as positive"
	else:
		print "Sentence is classified as negative"

	#don't forget to store your hard trained model
	store_model("example.pickle",classifier)
