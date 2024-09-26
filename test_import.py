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

user_id = bot.get_user_id()
print(f"My user ID is: {user_id}")





# Set your Twitter API credentials



