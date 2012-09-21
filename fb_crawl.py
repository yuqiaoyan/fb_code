from fb_retrieve import *
import facebook

access_token=open('out/facebook.access_token').read()

#forbes FB page ID
fb_id = get_page_id('nytimes')

fb_api = facebook.GraphAPI(access_token)

#get post data for Forbes
#fb_response = fb_api.get_connections(fb_id,"posts")

#Sample query SELECT uid, rsvp_status FROM event_member WHERE eid=12345678

query = "SELECT message, attachment, likes, message_tags, description, description_tags, type FROM stream WHERE source_id= %s and created_time > 1262196000 LIMIT 50" % fb_id

fqldata = fb_api.fql(query) 

#fb_response.keys = ['paging','data']
#data = fb_response['data']
#next_page = fb_response['paging']
