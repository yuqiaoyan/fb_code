from my_tokenizers import *
import nltk
import os
import argparse
import pandas as pd
import sys
import random

script_path = "/home/ubuntu/fb_code"
sys.path.append(script_path)

from fb_process import *

#### PARSE COMMAND LINE ARGUMENTS ####
parser = argparse.ArgumentParser(description='test classifiers on facebook data')
parser.add_argument('--filepath', default = 'training.txt',help='set filepath for training data')
parser.add_argument('--classifier',default = 'lj_emote_classifier.pickle')
args = parser.parse_args()

def store_model(filepath, data):
	'''REQUIRES: filepath and data
	PURPOSE: allows me to save my models for later usage
	'''
	import pickle
	f = open(filepath,'wb')
	pickle.dump(data,f)
	f.close()

def load_model(filepath):
	import pickle
	f = open(filepath);
	model = pickle.load(f)
	f.close()
	return(model)

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

	#use the top 70000 most frequent words for our training data
	vocabulary = word_distribution.keys()[:70000]

	return vocabulary

def extract_feature_presence(document):
	'''REQUIRES: set of vocabulary words and tokenized document list 
	RETURNS: dictionary of words and whether or not it's present
	{'cat': false
	 'dog': true
	 ...}
	 '''
	#get all word features
	vocabulary = get_word_features_set(args.filepath)

	#getting all unique words from each document
	#this extracts word features for a binomial classifier
	#document_words = tokenize_sentence_emote(document) 
	document_words = set(document)


	word_features = {}
	
	for word in vocabulary:
		word_features[word] = (word in document_words)

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


def train_classifier(filepath = "training.txt"):
#sample code to show how to run the classifier

	import time
	start = time.clock()

	vocabulary = get_word_features_set(filepath)
	training_set = get_nltk_training_set(filepath)
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	elapsed = (time.clock()-start)

	print "Classifier training time is %s s " % elapsed
	label = classifier.classify(extract_feature_presence(tokenize_sentence_emote("this is a test.. !!!")))
	
	if(label == 1):
		print "Sentence is classified as positive"
	else:
		print "Sentence is classified as negative"

	#don't forget to store your hard trained model
	store_model("lj_70000_emote_classifier.pickle",classifier)
	store_model("lj_70000_vocabulary.pickle",vocabulary)


def validate_classifier():
	nytimes = get_collection_df("comments","nytimes")
	kansas = get_collection_df("comments","kansascitystar")
	paper_posts = nytimes.append(kansas,ignore_index=True)

	paper_posts.index = range(0,len(paper_posts))
	#paper_posts = paper_posts.reset_index()

	print paper_posts.index

	#filter and label all messages related to obama and romney
	paper_posts['political_affiliation'] = paper_posts['message'].map(lambda x: label_political_affilication(x))
	paper_posts = paper_posts[paper_posts['political_affiliation'] != 'none']

	#get a list of random integers so we can index by them
	rand_list = np.random.randint(0,len(paper_posts)-1,200)
	rand_list = random.sample(range(0,len(paper_posts-1)),200)

	#get 200 random comments for validation
	test_posts = paper_posts.take(rand_list)
	test_posts_small = test_posts[['message','created_time','post_id','political_affiliation']]
	print test_posts_small.index


	post_list = [] #maintains the facebook post content associated with the comment so we can validate later


	#get post that propogated this comment
	db = initConnection("fb_train")
	for index,post_id in test_posts_small['post_id'].iteritems():
		fb_cursor = db.posts.find({'id':post_id})

		#each comment should retrieve one post
		if(fb_cursor.count() == 1):
			comment_post = [x for x in fb_cursor][0]

			#if there is no description set it to empty
			if(comment_post.get('description') == None): comment_post['description']=""

			#if there is no message content set it to empty
			if(comment_post.get('message') == None): comment_post['message']=""
			post_list.append(comment_post['message']+" "+comment_post['description'])
		elif(fb_cursor.count() == 0):
			print "error: no post was found"
		else:
			print "error: duplicates were found"
		#print "this is the comment's post",comment_post

	test_posts_small['post_content']= post_list
		
	test_posts_small.to_csv("sentiment/validation/political_comments_for_validation.csv",encoding = "utf-8",index=False)
	classifier = load_model(args.classifier)
	test_posts_small['lj_emote_classifier']=test_posts_small['message'].map(lambda x: classifier.classify(extract_feature_presence(tokenize_sentence_emote(x))))
	test_posts_small.to_csv("sentiment/validation/political_comments_lj_classified.csv", encoding = "utf-8",index=False)
		#return comment_post

if __name__ == '__main__':
	validate_classifier()
	#train_classifier()
