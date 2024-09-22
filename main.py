import os
from writefile import MySQLWriter
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

# Initialize MySQLWriter and print success message on connection
try:
    db_writer = MySQLWriter(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), database=os.getenv('database'))
    print("Connected to MySQL database successfully.")
except Exception as e:
    print(f"Failed to connect to MySQL: {e}")
    exit()

# Read existing data
existing_data = db_writer.read_existing_followings()  # Updated to read followings
existing_blockedList = db_writer.read_existing_blockings()  # Updated to read blockings
existing_mutedlist = db_writer.read_existing_mutings()    # Updated to read mutings

# Lists to hold new entries
new_followings = []
new_blockings = []
new_muting = []

while True:
    for address in addressList:
        efp_user = FollowAndTags(address)
        efp_user_link = efp_user.get_following_url()

        get_addy = Follows(efp_user_link)

        try:
            addresses = get_addy.extract_addresses()
            existing_addresses = existing_data.get(address, set())
            new_addresses = set(addresses) - existing_addresses
            if new_addresses:
                new_followings.append({address: new_addresses})
                print(f"New followings found for {address}: {new_addresses}")
            else:
                print(f"No new followings found for {address}")

        except requests.HTTPError as e:
            print(f"Error occurred: {e}")

        efp_block_tag = efp_user.get_tags_url()
        get_block_tag = Follows(efp_block_tag)

        AllTags = get_block_tag.extract_tags()

        try:
            BlockedUsers = Blocks(AllTags)
            listofBlockusers = BlockedUsers.extract_block_users()
            existing_blockedusers = existing_blockedList.get(address, set())
            new_blocked_addresses = set(listofBlockusers) - existing_blockedusers

            if new_blocked_addresses:
                new_blockings.append({address: new_blocked_addresses})
                print(f"New blockings found for {address}: {new_blocked_addresses}")
            else:
                print(f"No new blockings found for {address}")

        except requests.HTTPError as e:
            print(f"Error occurred: {e}")

        try:
            MutedUsers = Mutes(AllTags)
            listofMutedusers = MutedUsers.extract_mute_users()
            existing_mutedUsers = existing_mutedlist.get(address, set())
            new_muted_addresses = set(listofMutedusers) - existing_mutedUsers

            if new_muted_addresses:
                new_muting.append({address: new_muted_addresses})
                print(f"New mutings found for {address}: {new_muted_addresses}")
            else:
                print(f"No new mutings found for {address}")

        except requests.HTTPError as e:
            print(f"Error occurred: {e}")

    # Process new followings
    for new_entry in new_followings:
        for address, addresses in new_entry.items():
            for new_addr in addresses:
                ensurl = EnsUrl(new_addr)
                get_ensurl = ensurl.get_ens_data_url()
                fetchens = FetchEns(get_ensurl)
                name = fetchens.extract_ens()
                # bot.post_following_tweet(address, name)

    # Process new blockings
    for new_entry in new_blockings:
        for address, addresses in new_entry.items():
            for new_addr in addresses:
                ensurl = EnsUrl(new_addr)
                get_ensurl = ensurl.get_ens_data_url()
                fetchens = FetchEns(get_ensurl)
                name = fetchens.extract_ens()
                # bot.post_blocking_tweet(address, name)

    # Process new mutings
    for new_entry in new_muting:
        for address, addresses in new_entry.items():
            for new_addr in addresses:
                ensurl = EnsUrl(new_addr)
                get_ensurl = ensurl.get_ens_data_url()
                fetchens = FetchEns(get_ensurl)
                name = fetchens.extract_ens()
                # bot.post_muting_tweet(address, name)

    # Write new data to MySQL with print statements for status
    if new_followings:
        for new_entry in new_followings:
            for address, addresses in new_entry.items():
                for new_addr in addresses:
                    # Write to followings table
                    db_writer.write_data('followings', [[address, new_addr]])
        print("New followings written to MySQL.")

    if new_blockings:
        for new_entry in new_blockings:
            for address, addresses in new_entry.items():
                for new_addr in addresses:
                    # Write to blocking table
                    db_writer.write_data('blocking', [[address, new_addr]])
        print("New blockings written to MySQL.")

    if new_muting:
        for new_entry in new_muting:
            for address, addresses in new_entry.items():
                for new_addr in addresses:
                    # Write to muting table
                    db_writer.write_data('muting', [[address, new_addr]])
        print("New mutings written to MySQL.")
    else:
        print("no data to write")

    time.sleep(20 * 60)
