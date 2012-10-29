from db_help import *
import numpy as np
import pandas as pd
import datetime as dt
from sentiment.fb_classifier import *

def get_posts(paper):
	start = dt.datetime(2012,9,1)
	end = dt.datetime(2012,9,30)

	collection_name = "posts"
	db = initConnection("fb_train")
	#get WSJ posts in September
	#fb_cursor = db[collection_name].find({'name':'wsj','created_time_parsed':{'$gt':start,'$lt':end}},limit = 150)
	fb_cursor = db[collection_name].find({'name':paper,'created_time_parsed':{'$gt':start,'$lt':end}})
	posts = [x for x in fb_cursor]

	key_list = ['name','description','created_time_parsed','message','title']
	ct_list = ['likes','comments'] 
	fb_result = []
	new_post = {}

	for post in posts:
		for key in key_list:
			if(post.get(key)):
				new_post[key] = post[key]
			else:
				new_post[key]=""
		for key in ct_list:
			if(post.get(key)):
				new_post[key] = post[key]['count']
			else:
				new_post[key]=0
		new_post = {}
		fb_result.append(new_post)

	posts_df = pd.DataFrame(fb_result)
	posts_df = posts_df.dropna()
	return posts_df[['name','created_time_parsed','description','message','likes','comments']]

#get all posts from Septebmer from a democratic and republican paper to validate our
#classifier
nytimes = get_posts("nytimes")
kansas = get_posts("kansascitystar")
paper_posts = nytimes.append(kansas)

#get a list of 100 random integers so we can index by them
rand_list = np.random.randint(0,len(paper_posts)-1,100)

#get 100 random posts for validation
test_posts = paper_posts.take(rand_list)
test_posts['content']=test_posts['description']+" "+test_posts['message']
test_posts_small = test_posts[['content','name']]
#test_posts_small.to_csv("posts_for_validation.csv",encoding = "utf-8")
classifier = load_model("sentiment/lj_emote_classifier.pickle")
test_posts_small['lj_emote_classifier']=test_posts_small['content'].map(lambda x: classifier.classify(extract_feature_presence(tokenize_sentence_emote(x))))
test_posts_small.to_csv("validation/posts_lj_classified.csv", encoding = "utf-8")
