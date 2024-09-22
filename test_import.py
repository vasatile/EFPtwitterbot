import os
import requests
from twitterbot import TwitterBot
from requests_oauthlib import OAuth1

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Create an instance of TwitterBot
bot = TwitterBot(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

try:
    address = "jamesuche.eth"
    ens_name = "neweth.eth"
    bot.post_following_tweet(address, ens_name)
except requests.exceptions.RequestException as e:
    if e.response.status_code == 403:
        error_data = e.response.json()
        if error_data['errors'][0]['code'] == 187:
            print("Error: Duplicate tweet detected.")
        else:
            print(f"Error: {error_data['errors'][0]['message']}")
    else:
        print(f"Error: {e}")




# Set your Twitter API credentials



