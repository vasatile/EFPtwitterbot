import os
import requests
from FollowsAndTagsUrl import FollowAndTags
from follows import Follows
from ensurl import EnsUrl
from fetchens import FetchEns
from blocks import Blocks
from mutes import Mutes
from twitterbot import TwitterBot
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Your Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Create an instance of TwitterBot
bot = TwitterBot(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Load the ENS names from the JSON file with utf-8 encoding
with open('noteworthyens.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Access the ENS names list
addressList = data['ens_names']

# Lists to hold new entries
new_followings = []
new_blockings = []
new_muting = []

def process_followings(address):
    efp_user = FollowAndTags(address)
    efp_user_link = efp_user.get_following_url()
    get_addy = Follows(efp_user_link)

    try:
        addresses = get_addy.extract_addresses()
        if addresses:
            new_addresses = addresses[0]  # Get the last element
            new_followings.append({address: new_addresses})
            logging.info(f"New followings found for {address}: {new_addresses}")
        else:
            logging.info(f"No new followings found for {address}")
    except (requests.HTTPError, IndexError) as e:
        logging.error(f"Error occurred while processing followings for {address}: {e}")

def process_blockings(address):
    efp_user = FollowAndTags(address)
    efp_block_tag = efp_user.get_tags_url()
    get_block_tag = Follows(efp_block_tag)

    AllTags = get_block_tag.extract_tags()

    try:
        BlockedUsers = Blocks(AllTags)
        listofBlockusers = BlockedUsers.extract_block_users()
        if listofBlockusers:
            new_blocked_addresses = listofBlockusers[0]  # Get the last element
            new_blockings.append({address: new_blocked_addresses})
            logging.info(f"New blockings found for {address}: {new_blocked_addresses}")
        else:
            logging.info(f"No new blockings found for {address}")
    except (requests.HTTPError, IndexError) as e:
        logging.error(f"Error occurred while processing blockings for {address}: {e}")

def process_mutings(address):
    efp_user = FollowAndTags(address)
    efp_block_tag = efp_user.get_tags_url()
    get_block_tag = Follows(efp_block_tag)

    AllTags = get_block_tag.extract_tags()

    try:
        MutedUsers = Mutes(AllTags)
        listofMutedusers = MutedUsers.extract_mute_users()
        if listofMutedusers:
            new_muted_addresses = listofMutedusers[0]  # Get the last element
            new_muting.append({address: new_muted_addresses})
            logging.info(f"New mutings found for {address}: {new_muted_addresses}")
        else:
            logging.info(f"No new mutings found for {address}")
    except (requests.HTTPError, IndexError) as e:
        logging.error(f"Error occurred while processing mutings for {address}: {e}")

def process_new_entries(new_followings, new_blockings, new_muting, bot):
    # Process new followings
    if new_followings:
        for new_entry in new_followings:
            for address, addresses in new_entry.items():
                if addresses:
                    ensurl = EnsUrl(addresses)
                    get_ensurl = ensurl.get_ens_data_url()
                    fetchens = FetchEns(get_ensurl)
                    name = fetchens.extract_ens()
                    if name == "":
                        logging.warning(f"No ENS name found for address {address}")
                        continue
                    
                    bot.post_following_tweet(address, name)

    # Process new blockings
    if new_blockings:
        for new_entry in new_blockings:
            for address, addresses in new_entry.items():
                if addresses:
                    ensurl = EnsUrl(addresses)
                    get_ensurl = ensurl.get_ens_data_url()
                    fetchens = FetchEns(get_ensurl)
                    name = fetchens.extract_ens()
                    if name == "":
                        logging.warning(f"No ENS name found for blocking address {address}")
                        continue
                    
                    bot.post_blocking_tweet(address, name)

    # Process new mutings
    if new_muting:  
        for new_entry in new_muting:
            for address, addresses in new_entry.items():
                if addresses:
                    ensurl = EnsUrl(addresses)
                    get_ensurl = ensurl.get_ens_data_url()
                    fetchens = FetchEns(get_ensurl)
                    name = fetchens.extract_ens()
                    if name == "" or name is None:
                        logging.warning(f"No ENS name found for muting address {address}")
                        continue
                    
                    bot.post_muting_tweet(address, name)

# Call the function
while True:
    for address in addressList:
        process_followings(address)
        process_blockings(address)
        process_mutings(address)
        
    # Call the function to process new entries
    process_new_entries(new_followings, new_blockings, new_muting, bot)

    # Sleep for 30 minutes
    time.sleep(30 * 60)
