import requests
from requests_oauthlib import OAuth1Session
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TwitterBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret, bearer_token):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.bearer_token = bearer_token
        self.oauth = self.create_oauth_session()

    def create_oauth_session(self):
        """Create an OAuth1 session for posting tweets."""
        return OAuth1Session(self.api_key, self.api_secret_key, self.access_token, self.access_token_secret)

    def post_tweet(self, tweet):
        """Post a tweet using the Twitter API."""
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet}

        response = self.oauth.post(url, json=payload)

        if response.status_code == 201:
            logging.info("Tweet posted successfully!")
            time.sleep(15 * 60)  # wait 15 minutes after each tweet
        elif response.status_code == 429:  # Too Many Requests
            logging.warning("Rate limit exceeded. Waiting for 4 hours...")
            time.sleep(4 * 60 * 60)  # Wait for 4 hours
            self.post_tweet(tweet)  # Retry posting the tweet
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")

    def post_following_tweet(self, address, ens_name, get_twitter_tag, name_x):
        """Post a tweet about a new follower."""
        tweet = f"""
{address} @{get_twitter_tag} started following {ens_name} @{name_x} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)

    def post_blocking_tweet(self, address, ens_name, get_twitter_tag, name_x):
        """Post a tweet about a new blocker."""
        tweet = f"""
{address} @{get_twitter_tag} just blocked {ens_name} @{name_x} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)

    def post_muting_tweet(self, address, ens_name, get_twitter_tag, name_x):
        """Post a tweet about a new mute."""
        tweet = f"""
{address} @{get_twitter_tag} just muted {ens_name} @{name_x} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)
