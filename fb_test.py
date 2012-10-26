from fb_retrieve import *
import facebook
import datetime
import time

access_token=open('out/facebook.access_token').read()

#forbes FB page ID
fb_id = get_page_id('nytimes')

fb_api = facebook.GraphAPI(access_token)
subscribers = fb_api.get_object(fb_id)['likes']

today = datetime.datetime.utcnow()
today_string = today.strftime('%Y-%m-%d')
endline = '\n'

filepath = "data/daily_likes.txt"
with open(filepath,'w') as f:
	header = ['date','pagename','likes','\n']
	header_string = '\t'.join(header)
	f.write(header_string)

	info = [today_string,'nytimes',str(subscribers),endline]
	info_line = '\t'.join(info)
	f.write(info_line)

#get post data for Forbes
#fb_response = fb_api.get_connections(fb_id,"posts")

#Sample query SELECT uid, rsvp_status FROM event_member WHERE eid=12345678

#query = "SELECT message, attachment, likes, message_tags, description, description_tags, type FROM stream WHERE source_id= %s and created_time > 1262196000 LIMIT 50" % fb_id

#fqldata = fb_api.fql(query) 

print "test"

#fb_response.keys = ['paging','data']
#data = fb_response['data']
#next_page = fb_response['paging']
