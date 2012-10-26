from fb_retrieve import *
import facebook
import datetime
import time

def get_paper_list(filepath):

	f = open(filepath,'rU')

	fb_name = []
	for line in f:
		fb_name.append(line.strip().split(',')[0])
	
	return fb_name

access_token=open('out/facebook.access_token').read()

pagenames = get_paper_list("/home/ubuntu/fb_code/data/top_np_finalA.csv")
#forbes FB page ID
fb_ids = []

for pagename in pagenames:
	fb_ids.append({'pagename':pagename,'id':get_page_id(pagename)})

fb_api = facebook.GraphAPI(access_token)


one_week_after = datetime.datetime(2012,11,13)
today = datetime.datetime.utcnow()

filepath = "data/daily_likes.txt"

#write header information
with open(filepath,'a') as f:
	header = ['date','pagename','likes','\n']
	header_string = '\t'.join(header)

#crawl for the number of likes for paper every day up to one week after election
while(today < one_week_after):
	for fb_news in fb_ids:
		fb_id = fb_news['id']
		subscribers = fb_api.get_object(fb_id)['likes']

		today = datetime.datetime.utcnow()
		today_string = today.strftime('%Y-%m-%d')
		endline = '\n'

		#append to the current file
		with open(filepath,'a') as f:
			info = [today_string,'nytimes',str(subscribers),endline]
			info_line = '\t'.join(info)
			f.write(info_line)

		#wait one day until we crawl again
	time.sleep(86400)
