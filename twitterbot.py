import requests
from requests_oauthlib import OAuth1Session
import time

class TwitterBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.oauth = self.create_oauth_session()

    def create_oauth_session(self):
        """Create an OAuth1 session."""
        return OAuth1Session(self.api_key, self.api_secret_key, self.access_token, self.access_token_secret)

    def post_tweet(self, tweet):
        """Post a tweet using the Twitter API."""
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet}

        while True:
            response = self.oauth.post(url, json=payload)

            if response.status_code == 201:
                print("Tweet posted successfully!")
                break
            elif response.status_code == 429:  # Too Many Requests
                print("Rate limit exceeded. Waiting to retry...")
                time.sleep(15)  # Wait for a bit before retrying (adjust as needed)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                break

    def post_following_tweet(self, address, ens_name):
        """Post a tweet about a new follower."""
        tweet = f"🚨 NEW ALERT!! \n {address} started following {ens_name}\n Track and Follow wallets @efp"
        self.post_tweet(tweet)

    def post_blocking_tweet(self, address, ens_name):
        """Post a tweet about a new blocker."""
        tweet = f"🚨 NEW ALERT!! \n {address} just blocked {ens_name} \n Track and Follow wallets @efp"
        self.post_tweet(tweet)

    def post_muting_tweet(self, address, ens_name):
        """Post a tweet about a new mute."""
        tweet = f"🚨 NEW ALERT!! \n {address} just muted {ens_name}\n Track and Follow wallets @efp"
        self.post_tweet(tweet)
