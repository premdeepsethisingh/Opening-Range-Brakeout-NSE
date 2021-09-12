from kiteconnect import KiteConnect
#enter your api_key,api_secret,request_token and by running this python file  get access token.
api_key = ""
api_secret = ""
request_token = ""


kite = KiteConnect(api_key=api_key)
data = kite.generate_session(request_token, api_secret=api_secret)

print(data["access_token"])
