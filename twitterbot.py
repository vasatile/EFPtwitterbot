import requests
from requests_oauthlib import OAuth1Session
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        """Post a tweet using the Twitter API, avoiding duplicates."""
        # Check if the tweet has been posted before
        if self.is_duplicate_tweet(tweet):
            logging.info("Duplicate tweet found, not posting.")
            return
        
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet}

        response = self.oauth.post(url, json=payload)

        if response.status_code == 201:
            logging.info("Tweet posted successfully!")
            time.sleep(10 * 60)  # wait 10 minutes after each tweet
        elif response.status_code == 429:  # Too Many Requests
            logging.warning("Rate limit exceeded. Waiting for 4 hours...")
            time.sleep(4 * 60 * 60)  # Wait for 4 hours
            self.post_tweet(tweet)  # Retry posting the tweet
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")

    def is_duplicate_tweet(self, tweet_text):
        """Check if the tweet is a duplicate by querying the user's recent tweets."""
        url = "https://api.twitter.com/2/users/me/tweets"  # Adjust this endpoint to match Twitter API v2
        params = {
            "max_results": 5  # Check the last 5 tweets for duplicates (adjust as needed)
        }
        
        response = self.oauth.get(url, params=params)

        if response.status_code != 200:
            logging.error(f"Error fetching recent tweets: {response.status_code} - {response.text}")
            return False  # Assume it's not a duplicate if we can't fetch tweets

        recent_tweets = response.json().get('data', [])
        for recent_tweet in recent_tweets:
            if recent_tweet['text'].strip() == tweet_text.strip():
                return True  # Duplicate found

        return False

    def post_following_tweet(self, address, ens_name):
        """Post a tweet about a new follower."""
        tweet = f"""
{address} started following {ens_name} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)

    def post_blocking_tweet(self, address, ens_name):
        """Post a tweet about a new blocker."""
        tweet = f"""
{address} just blocked {ens_name} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)

    def post_muting_tweet(self, address, ens_name):
        """Post a tweet about a new mute."""
        tweet = f"""
{address} just muted {ens_name} @efp
        
https://ethfollow.xyz/{address}
"""
        self.post_tweet(tweet)
