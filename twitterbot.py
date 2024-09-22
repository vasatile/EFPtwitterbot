import requests
from requests_oauthlib import OAuth1Session

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
        """Post a tweet using the Twitter API and handle errors."""
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet}
        
        try:
            response = self.oauth.post(url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            print("Tweet posted successfully!")
        except requests.exceptions.RequestException as e:
            self.handle_tweet_error(e)

    def handle_tweet_error(self, e):
        """Handle errors when posting a tweet."""
        if e.response:
            if e.response.status_code == 403:
                error_data = e.response.json()
                if error_data['errors'][0]['code'] == 187:  # Duplicate tweet error
                    print("Error: Duplicate tweet detected.")
                else:
                    print(f"Error: {error_data['errors'][0]['message']}")
            else:
                print(f"Error: {e.response.status_code} - {e.response.text}")
        else:
            print(f"Error: {e}")

    def upload_media(self, image_path):
        """Upload an image to Twitter and return the media ID."""
        try:
            media = self.api.media_upload(image_path)
            return media.media_id_string
        except Exception as e:
            print(f"Failed to upload media: {e}")
            return None

    def post_following_tweet(self, address, ens_name, image_path):
        """Post a tweet about a new follower."""
        tweet = f"{address} just started following {ens_name}.\nTrack and follow address with @efp"
        media_id = self.upload_media(image_path)
        if media_id:
            self.oauth.post("https://api.twitter.com/2/tweets", json={"text": tweet, "media_ids": [media_id]})
        else:
            self.post_tweet(tweet)

    def post_blocking_tweet(self, address, ens_name, image_path):
        """Post a tweet about a new block."""
        tweet = f"{address} just blocked {ens_name}.\nTrack and follow address with @efp"
        media_id = self.upload_media(image_path)
        if media_id:
            self.oauth.post("https://api.twitter.com/2/tweets", json={"text": tweet, "media_ids": [media_id]})
        else:
            self.post_tweet(tweet)

    def post_muting_tweet(self, address, ens_name, image_path):
        """Post a tweet about a new mute."""
        tweet = f"{address} just muted {ens_name}.\nTrack and follow address with @efp"
        media_id = self.upload_media(image_path)
        if media_id:
            self.oauth.post("https://api.twitter.com/2/tweets", json={"text": tweet, "media_ids": [media_id]})
        else:
            self.post_tweet(tweet)
