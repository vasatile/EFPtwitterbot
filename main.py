import os
import psycopg2
from urllib.parse import urlparse
from writefile import PostgresWriter
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

if not all([API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    logging.error("One or more Twitter API credentials are missing.")
    exit(1)

# Create an instance of TwitterBot
bot = TwitterBot(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Load the ENS names from the JSON file with utf-8 encoding
try:
    with open('noteworthyens.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Access the ENS names list
    addressList = data['ens_names']
    logging.info("ENS names loaded successfully.")
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    exit(1)
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON: {e}")
    exit(1)

# Parse Heroku DATABASE_URL (or use local PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Parse the Heroku PostgreSQL URL
    url = urlparse(DATABASE_URL)
    db_host = url.hostname
    db_user = url.username
    db_password = url.password
    db_name = url.path[1:]  # Remove the leading "/"
else:
    logging.error("DATABASE_URL environment variable is not set.")
    exit(1)

# Initialize PostgresWriter with the Heroku DB credentials
try:
    db_writer = PostgresWriter(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    logging.info("Connected to PostgreSQL database successfully.")
except Exception as e:
    logging.error(f"Failed to connect to PostgreSQL: {e}")
    exit(1)

# Read existing data
try:
    existing_data = db_writer.read_existing_followings()
    existing_blockedList = db_writer.read_existing_blockings()
    existing_mutedlist = db_writer.read_existing_mutings()
    logging.info("Existing data successfully loaded from the database.")
except Exception as e:
    logging.error(f"Error reading existing data: {e}")
    exit(1)

# Add more logic here if necessary...


# Lists to hold new entries as sets to avoid duplicates
new_followings = set()
new_blockings = set()
new_muting = set()



def process_followings(address):
    logging.info(f"Processing followings for {address}...")
    efp_user = FollowAndTags(address)
    efp_user_link = efp_user.get_following_url()
    get_addy = Follows(efp_user_link)

    attempt = 0
    while attempt < 3:  # Try up to 3 times
        try:
            addresses = get_addy.extract_addresses()
            logging.info(f"Fetched addresses: {addresses}")

            if addresses:
                existing_addresses = existing_data.get(address, set())

                latest_follow = addresses[0]  # Get the last element
                logging.info(f"Latest follow address: {latest_follow}")

                new_addresses = {latest_follow} - existing_addresses

                if new_addresses:
                    single_address = list(new_addresses)[0]
                    new_followings.add((address, single_address))  # Add as tuple to set
                    logging.info(f"New followings found for {address}: {single_address}")
                else:
                    logging.info(f"No new followings found for {address}")
            else:
                logging.info(f"No addresses found for {address}")
            break  # Exit loop if successful
        except Exception as e:
            attempt += 1
            logging.error(f"Error occurred while processing followings for {address}: {e}")
            if attempt < 3:
                logging.info(f"Retrying... attempt {attempt}")
                time.sleep(2)  # Wait before retrying
            else:
                logging.error(f"Failed to process followings for {address} after 3 attempts")


def process_blockings(address):
    efp_user = FollowAndTags(address)
    efp_block_tag = efp_user.get_tags_url()
    get_block_tag = Follows(efp_block_tag)

    attempt = 0
    while attempt < 3:  # Try up to 3 times
        try:
            AllTags = get_block_tag.extract_tags()
            BlockedUsers = Blocks(AllTags)
            listofBlockusers = BlockedUsers.extract_block_users()
            if listofBlockusers:
                existing_blockedusers = existing_blockedList.get(address, set())
                latest_blocked_addresses = listofBlockusers[0]
                new_blocked_addresses = {latest_blocked_addresses} - existing_blockedusers
                if new_blocked_addresses:
                    single_blocked_address = list(new_blocked_addresses)[0]
                    new_blockings.add((address, single_blocked_address))  # Add as tuple to set
                    logging.info(f"New blockings found for {address}: {single_blocked_address}")
            else:
                logging.info(f"No new blockings found for {address}")
            break  # Exit loop if successful

        except Exception as e:
            attempt += 1
            logging.error(f"Error occurred while processing blockings for {address}: {e} (Attempt {attempt}/3)")
            if attempt < 3:
                time.sleep(2)  # Wait before retrying
            else:
                logging.error(f"Failed to process blockings for {address} after 3 attempts")
                

def process_mutings(address):
    efp_user = FollowAndTags(address)
    efp_block_tag = efp_user.get_tags_url()
    get_block_tag = Follows(efp_block_tag)

    AllTags = get_block_tag.extract_tags()
    
    attempt = 0
    while attempt < 3:  # Try up to 3 times
        try:
            MutedUsers = Mutes(AllTags)
            listofMutedusers = MutedUsers.extract_mute_users()
            if listofMutedusers:
                existing_mutedUsers = existing_mutedlist.get(address, set())
                latest_muted_addresses = listofMutedusers[0]  # Get the last element
                new_muted_addresses = {latest_muted_addresses} - existing_mutedUsers
                if new_muted_addresses:
                    single_muted_address = list(new_muted_addresses)[0]
                    new_muting.add((address, single_muted_address))  # Add as tuple to set
                    logging.info(f"New mutings found for {address}: {single_muted_address}")
            else:
                logging.info(f"No new mutings found for {address}")
            break
        except Exception as e:
            attempt += 1
            logging.error(f"Error occurred while processing mutings for {address}: {e}")
            if attempt < 3:
                time.sleep(2)  # Wait before retrying
            else:
                logging.error(f"Failed to process mutings for {address} after 3 attempts")
                
def process_new_entries(new_followings, new_blockings, new_muting, bot):
    # Process new followings
    for address, new_address in new_followings:
        if new_address:
            ensurl = EnsUrl(new_address)
            get_ensurl = ensurl.get_ens_data_url()
            fetchens = FetchEns(get_ensurl)
            name = fetchens.extract_ens()
            name_x = fetchens.extract_xtag()
            
            if name == "" or name is None:
                logging.warning(f"No ENS name found for address {address}")
                continue
            
            ensurl_xtag = EnsUrl(address)
            get_ensurl_xtag = ensurl_xtag.get_ens_data_url()
            fetchens_xtag = FetchEns(get_ensurl_xtag)
            get_twitter_tag = fetchens_xtag.extract_xtag()
            
            if get_twitter_tag == "" or get_twitter_tag is None:
                logging.warning(f"no x handle for {address}")
                continue
            
            # bot.post_following_tweet(address, name, get_twitter_tag, name_x)

    # Process new blockings
    for address, new_address in new_blockings:
        if new_address:
            ensurl = EnsUrl(new_address)
            get_ensurl = ensurl.get_ens_data_url()
            fetchens = FetchEns(get_ensurl)
            name = fetchens.extract_ens()
            if name == "" or name is None:
                logging.warning(f"No ENS name found for blocking address {address}")
                continue
            
            # bot.post_blocking_tweet(address, name)

    # Process new mutings
    for address, new_address in new_muting:  
        if new_address:
            ensurl = EnsUrl(new_address)
            get_ensurl = ensurl.get_ens_data_url()
            fetchens = FetchEns(get_ensurl)
            name = fetchens.extract_ens()
            if name == "" or name is None:
                logging.warning(f"No ENS name found for muting address {address}")
                continue
            
            # bot.post_muting_tweet(address, name)

def update_data(new_followings, new_blockings, new_muting):
    if new_followings:
        for address, new_addr in new_followings:
            # Write to followings table
            db_writer.write_data('followings', [[address, new_addr]])
        print("New followings written to PostgreSQL.")

    if new_blockings:
        for address, new_addr in new_blockings:
            # Write to blocking table
            db_writer.write_data('blocking', [[address, new_addr]])
        print("New blockings written to PostgreSQL.")

    if new_muting:
        for address, new_addr in new_muting:
            # Write to muting table
            db_writer.write_data('muting', [[address, new_addr]])
        print("New mutings written to PostgreSQL.")
    else:
        print("No data to write")


# Call the function
while True:
    for address in addressList:
        process_followings(address)
        process_blockings(address)
        process_mutings(address)
        
    # Call the function to process new entries
    process_new_entries(new_followings, new_blockings, new_muting, bot)
    update_data(new_followings, new_blockings, new_muting)

    # Clear the new entries after processing
    new_followings.clear()
    new_blockings.clear()
    new_muting.clear()

    # Sleep for 30 minutes
    time.sleep(50 * 60)