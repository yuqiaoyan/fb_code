import time
from fb_retrieve import *
import facebook
import urllib
import pymongo
import json
import datetime
from dateutil.parser import parse
from db_help import *
import multiprocessing

#GLOBALS
FB_MAX_QUERIES = 600 #600 queries per IP per token per seconds hitting FB API
access_token=open('out/facebook.access_token').read()

############### FB HELPERS #####################
def get_comments(post_id,access_token):
#requires a fb access_token and a fb post_id
#returns a tuple: a page of comments and the cursor to the next set of comments
#the max comments is 25 per page
	url = 'https://graph.facebook.com/'+post_id+'/comments?access_token='+access_token
	response = json.load(urllib.urlopen(url))
	if(response.get('data')==None):
		comments = ''
	else:
		comments = response['data']

	if(response.get('paging')==None):
		next_comments = ''
	elif(response['paging'].get('next')==None):
		next_comments = ''
	else:
		next_comments = response['paging']['next']
	
	return comments,next_comments

def get_next(next_page):
#requires the url of the next_page
#gets the next page of response data (comments, posts, etc)
#returns a tuple of the data and the next_page
	response = json.load(urllib.urlopen(next_page))

	if(response.get('paging')==None):
		return None,None

	if(response['paging'].get('next')==None):
		return None,None

	return response['data'],response['paging']['next']

def add_to_list_data(a_list, key, value):
	for data in a_list:
		data[key]=value
	return a_list

def get_comments_from_post(post_id,num_comments,num_queries,db,pagename):
	print "%s has %s number of comments" % (post_id, num_comments)
	num_queries+=1
	curr = datetime.datetime.utcnow()
	comments,next_comments = get_comments(post_id,access_token)
	comments = add_to_list_data(comments,'post_id',post_id)
	comments = add_to_list_data(comments,'pagename',pagename)
	comments = add_to_list_data(comments,'time',curr)
	
	if(len(comments)>0):
		db.comments.insert(comments)
	
	while(len(comments)>0):
		comments,next_comments = get_next(next_comments)
		num_queries+=1
		
		#FB bug?  and sometimes does not provide Next
		if(comments):
			curr = datetime.datetime.utcnow()
			comments = add_to_list_data(comments,'post_id',post_id)
			comments = add_to_list_data(comments,'pagename',pagename)
			comments = add_to_list_data(comments,'time',curr)
			last_comment_id = comments[len(comments)-1]['id']
			
			if(db.comments.find({'id':last_comment_id}).count()==0):
				db.comments.insert(comments)

		if(next_comments == None or comments == None):
			break

	return num_queries

###############DB
def get_fb_list(db,collection_name = "posts",num_results=None):
	num_results = 0
	fb_cursor = db[collection_name].find(limit = num_results)
	fb_list = [post for post in fb_cursor]
	#TODO: Flatten the data. Identify the data I want when I analyze it
	#Make it easy to show all the data to qiaozhu using ipython notebook

	return fb_list

def insert_post_data(posts,next_page_url,num_queries):
	start = datetime.datetime.utcnow()

	num_posts = 0
	#while there is still posts left, collect the posts
	while(num_posts < 100):
		
		if(len(posts)==0): break
		if(num_queries > FB_MAX_QUERIES):
			curr = datetime.datetime.utcnow()
			time_delta = curr-start
			time_delta = time_delta.total_seconds()
			
			#if we hit the FB rate limit, then wait before we query again 
			if(time_delta < 600):
				num_queries = 0
				time.sleep(600 - time_delta + 100) #add 100 second buffer
			#if it took more than an hour, then reduce num_queries based on hr
			else:
				num_queries = int(num_queries*(time_delta/600))

			start = datetime.datetime.utcnow()

		try:
			for post in posts:
				post['pagename']=pagename
				post['time']=datetime.datetime.utcnow()
				post['created_time_parsed']=parse(post.get('created_time',None))
				if(post.get('comments')!= None):
					num_comments = post['comments'].get('count',0)
					#if there are more than 0 comments, let's grab up to 50 comments per post
				if(num_comments>0):
					post_id = post['id']
					num_queries = get_comments_from_post(post_id,num_comments,num_queries,db,pagename)

			db.posts.insert(posts);
			posts,next_page_url = get_next(next_page_url)
			num_posts = num_posts + 25
			num_queries +=1
			print "number of queries is",num_queries
		except Exception, inst:
			print "Exception raised for", pagename
			print type(inst)
			print "With this args", inst.args

def crawl(db,fb_news):
#request and insert facebok post data into mongo db

	num_queries = 0
	
	pagename = fb_news['pagename']
	fb_id = fb_news['id']
	print "Getting page data for",pagename 
	#get post data from the news property
	fb_response = fb_api.get_connections(fb_id,"posts")
	num_queries+=1

	posts = fb_response['data']
	next_page_url = fb_response['paging']['next']
	insert_post_data(posts,next_page_url,num_queries)

		

def get_paper_list(filepath):

	f = open(filepath,'rU')

	fb_name = []
	for line in f:
		fb_name.append(line.strip().split(',')[0])
	
	return fb_name

############### MAIN ##########################

#connect to the db fb_train
db = initConnection("fb_crawl")


#get token and connect to the graph API
fb_api = facebook.GraphAPI(access_token)

pagenames = get_paper_list("/home/ubuntu/fb_code/data/top_np_finalA.csv")

#pagenames = ["wsj","kansascitystar","theoregonian","TampaTribune","denverpost","thenewyorkdailynews","orlandosentinel","chicagotribune","nytimes","saltlaketribune","washingtonpost"]
fb_ids = []

for pagename in pagenames:
	fb_ids.append({'pagename':pagename,'id':get_page_id(pagename)})

for fb_news in fb_ids:
	multiprocessing.Process(target = crawl,args=[db,fb_news]).start()
################# FQL EXAMPLE ##############
#Sample query SELECT uid, rsvp_status FROM event_member WHERE eid=12345678

#query = "SELECT message, attachment, likes, message_tags, description, description_tags, type FROM stream WHERE source_id= %s and created_time > 1262196000 LIMIT 50" % fb_id

#fqldata = fb_api.fql(query) 
