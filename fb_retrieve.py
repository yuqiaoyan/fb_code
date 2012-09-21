import urllib
import json
import webbrowser
import os
import sys

#this file provides a few helper functions to acquire data from facebook

def get_access_token(CLIENT_ID,REDIRECT,EXTENDED_PERMS):
#open a browser window to get an access token specified by the client id,redirect and extended_permsl
#TODO: Look up token expiration and handle that
#user is required to manually input access token 

	args = dict(client_id = CLIENT_ID,redirect_uri=REDIRECT,scope=','.join(EXTENDED_PERMS),type='user_agent',display='popup')

	webbrowser.open('http://graph.facebook.com/oauth/authorize?'+urllib.urlencode(args))

	access_token = raw_input('Enter your access token: ')

	#write the access token to a text file
	if not os.path.isdir('out'):
		os.mkdir('out')

	filename = os.path.join('out','facebook.access_token')
	f=open(filename,'w')
	f.write(access_token)
	f.close()

	return access_token

def pretty_dict(a_json,filename):
#given a_json dictionary type, print the json beautifully
	f = open(filename,'w')
	json.dump(a_json,f,sort_keys=False,indent=4)
	f.close()

def get_page_profile(pageName):
#get a FB page's profile data and return it as a dictionary
	response = urllib.urlopen('https://graph.facebook.com/'+pageName).read()
	pageProfileDict = json.loads(response)
	return(pageProfileDict)

def get_page_id(page_name):
#given the page name of 
	page_profile_dict = get_page_profile(page_name)
	return page_profile_dict['id']

