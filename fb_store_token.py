from fb_retrieve import *
import facebook

#app_id = "168537696510622"
#app_secret = "a1318fd1906d912538c05ccb43b527c4"

app_id = "355139764567287"
app_secret = "9abbd7a77b622219b393685019e179c1"

redirect_uri = "http://www.dance25.com"
extended_perms = []

access_token = get_access_token(app_id,redirect_uri,extended_perms)
fb_api = facebook.GraphAPI(access_token)
token_response = fb_api.extend_access_token(app_id,app_secret)
