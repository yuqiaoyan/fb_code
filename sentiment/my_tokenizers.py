import re
import nltk.corpus

#exception = "\xe2\x80\x99\x93"
#word_pattern = re.compile(r"[a-zA-Z'-%s]+|[?!]"%exception)
word_pattern = re.compile(r"[a-zA-Z'-]+|[^\w\s]+")

def tokenize_sentence_emote(sentence, unique_stop_words=[]):
	'''REQUIRES: string sentence to tokenized
	OPTIONAL: unique_stop_words, to define your own unique_stop_words for your corpus
	RETURNS: list of tokens
		words without punctuation
		emoticons is captured
		stop words is excluded
	EXAMPLE: 
		input = 'hi! this is a test... !!!'
		output = ['hi','test','..','!!!'] 
	'''
	word_list = word_pattern.findall(sentence)
	tokenized_word_list = []

	stopwords = nltk.corpus.stopwords.words('english')	
	stopwords = stopwords + unique_stop_words

	for word in word_list:
		word = word.lower()
		if word not in stopwords and len(word) > 1:
			tokenized_word_list.append(word)
	return(tokenized_word_list)

def tokenize_sentence(sentence,unique_stop_words=[]):
	'''REQUIRES: a sentence
	unique_stop_words is a list of additional stop words you define e.g. ['wall','street']
	RETURNS: a list of tokens split by spaces without stop words
	'''
	words = []

	for word in sentence.split(' '):
		stopwords = nltk.corpus.stopwords.words('english')
		stopwords = stopwords + unique_stop_words 
		if not word.lower() in stopwords and len(word) > 2:
			words.append(word.lower())

	return words

#def tokenize_text_list(text_list,unique_stop_words=[]):
#	'''REQUIRES: text_list is a list of sentences; unique_stop_words is a list of additional stopwords you can define
#	RETURNS: a list of tokens without stop words
#	'''
	#words = []
    #for text in text_list:
        #text = text.strip()
        #words = [word.lower() for word in text.split(' ') if not word.lower() in nltk.corpus.stopwords.words('english')]
        #for word in text.split(' '):
            #stopwords = nltk.corpus.stopwords.words('english')
            #stopwords = stopwords + unique_stop_words 
            #if not word.lower() in stopwords:
                #words.append(word.lower())
    #return words