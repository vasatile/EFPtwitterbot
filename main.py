import os
import requests
from FollowsAndTagsUrl import FollowAndTags
from follows import Follows
from ensurl import EnsUrl
from fetchens import FetchEns
from blocks import Blocks
from mutes import Mutes
from writefile import CSVWriter
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




csv_writer = CSVWriter('followings.csv')
blockList_writer = CSVWriter("blocked_list.csv")
mutedList_writer = CSVWriter("muted_list.csv")

#Read existing data
existing_data = csv_writer.read_existing_data()
existing_blockedList = blockList_writer.read_existing_data()
existing_mutedlist = mutedList_writer.read_existing_data()


# List to hold all rows to write to blocked CSV
blocked_list = []

# List to hold all rows to write to followings CSV
data_to_write = []  

# List to hold all rows to write to muted CSV
muted_list = []

new_followings = []
new_blockings = []
new_muting = []

while True:
    
    for address in addressList:
        

        efp_user = FollowAndTags(address)
        efp_user_link = efp_user.get_following_url()
        # print(efp_user_link)

        get_addy = Follows(efp_user_link)

        try:
            addresses = get_addy.extract_addresses()
            # print(f"Extracted addresses for {address}: {addresses}")
            
            # Initialize existing_addresses to an empty set
            existing_addresses = existing_data.get(address, set())  # Get existing addresses or an empty set

            # Compare with existing data
            if address in existing_data:
                existing_addresses = existing_data[address]
                new_addresses = set(addresses) - existing_addresses  # Find new addresses
                new_followings.append({address:(new_addresses)})
                
            else:
                
                new_addresses = set(addresses)  # All are new if address is not in existing data

            if new_addresses:
                
                # Create a row with the main address followed by its updated addresses
                row_data = [address] + list(existing_addresses.union(new_addresses))
                data_to_write.append(row_data)  # Add to the list for writing later
            else:
                # print(f"No new data for {address}.")
                pass
        
        except requests.HTTPError as e:
            print(f"Error occurred: {e}")



        

    
        


        efp_block_tag = efp_user.get_tags_url()
        get_block_tag = Follows(efp_block_tag)

        AllTags = get_block_tag.extract_tags()
        # print(AllTags)

        try:
            
            BlockedUsers = Blocks(AllTags)
            listofBlockusers = BlockedUsers.extract_block_users()
            # print(listofBlockusers)
            
            # Initialize existing_addresses to an empty set
            existing_blockedusers = existing_blockedList.get(address, set())  # Get existing addresses or an empty set
            if address in existing_blockedList:
                existing_blockedusers = existing_blockedList[address]
                new_blocked_addresses = set(listofBlockusers) - existing_blockedusers #finds new addresses blocked
                new_blockings.append({address:(new_blocked_addresses)})
                
            else:
                new_blocked_addresses = set(listofBlockusers)
                
                
            if new_blocked_addresses:
                # Print the key (address) and the new addresses
                    print(f"New addresses for {address}: {new_blocked_addresses}")
                    # Create a row with the main address followed by its updated addresses
                    block_row = [address] + list(existing_blockedusers.union(new_blocked_addresses))
                    blocked_list.append(block_row)  # Add to the list for writing later
                    
            else:
                    # print(f"No new data for {address}.")
                    pass
            
        except requests.HTTPError as e:
                print(f"Error occurred: {e}")



        # block_row = [address]+listofBlockusers
        # blocked_list.append(block_row)
        

        
        try:
                
                MutedUsers = Mutes(AllTags)
                listofMutedusers = MutedUsers.extract_mute_users()
                # print(listofMutedusers)
                
                # Initialize existing_addresses to an empty set
                existing_mutedUsers = existing_mutedlist.get(address, set())  # Get existing addresses or an empty set
                if address in existing_mutedlist:
                    existing_mutedUsers = existing_mutedlist[address]
                    new_muted_addresses = set(listofMutedusers) - existing_mutedUsers #finds new addresses muted
                    new_blockings.append({address:(new_muted_addresses)})
                    
                else:
                    new_muted_addresses = set(listofMutedusers)
                    
                    
                if new_muted_addresses:
                    
                        # Print the key (address) and the new addresses
                        print(f"New addresses for {address}: {new_muted_addresses}")
                        # Create a row with the main address followed by its updated addresses
                        muted_row = [address] + list(existing_mutedUsers.union(new_muted_addresses))
                        muted_list.append(muted_row)  # Add to the list for writing later
                    
                else:
                        # print(f"No new data for {address}.")
                        pass
                
        except requests.HTTPError as e:
                    print(f"Error occurred: {e}")


# Wait for 6 minutes (6 minutes = 6 * 60 seconds)
    

    
    
    
  
    


    # Iterate through the list and pick only the ones with non-empty values

    for new_entry in new_followings:
        for address, addresses in new_entry.items():
            if addresses:  # Check if the set of addresses is not empty
                    print(f"Address: {address}, New Addresses: {addresses}")
                    for new_addr in addresses:
                        # print(f"New Address: {new_addr}")

                        ensurl = EnsUrl(new_addr)

                        get_ensurl = ensurl.get_ens_data_url()
                        # print(get_ensurl)

                        fetchens = FetchEns(get_ensurl)
                        name = fetchens.extract_ens()
                    # print(f"{address} just followed {name}")
                    # Post a tweet about a new follower
                    bot.post_following_tweet(address, name)
                            


    for new_entry in new_blockings:
        for address, addresses in new_entry.items():
            if addresses:  # Check if the set of addresses is not empty
                    # print(f"Address: {address}, New Addresses: {addresses}")
                    for new_addr in addresses:
                        # print(f"New Address: {new_addr}")

                        ensurl = EnsUrl(new_addr)

                        get_ensurl = ensurl.get_ens_data_url()
                        # print(get_ensurl)

                        fetchens = FetchEns(get_ensurl)
                        name = fetchens.extract_ens()
                    # print(f"{address} just blocked {name}")
                    # Post a tweet about a new follower
                    bot.post_blocking_tweet(address, name)
                
            
            
            
    for new_entry in new_muting:
        for address, addresses in new_entry.items():
            if addresses:  # Check if the set of addresses is not empty
                    # print(f"Address: {address}, New Addresses: {addresses}")
                    for new_addr in addresses:
                        # print(f"New Address: {new_addr}")

                        ensurl = EnsUrl(new_addr)

                        get_ensurl = ensurl.get_ens_data_url()
                        # print(get_ensurl)

                        fetchens = FetchEns(get_ensurl)
                        name = fetchens.extract_ens()
                    # print(f"{address} just muted {name}")
                    # Post a tweet about a new follower
                    bot.post_muting_tweet(address, name)
                        
    # Check if there's any data to write before writing to CSV
    if data_to_write:
        csv_writer.write_data(data_to_write)
        
    else:
        # print("No new data to write. The CSV file remains unchanged.")
        pass
        
    if blocked_list:
        blockList_writer.write_data(blocked_list)
    else:
        # print("No new data to write. The CSV file remains unchanged.")
            pass
    if muted_list:
        mutedList_writer.write_data(muted_list)
    else:
        # print("No new data to write. The CSV file remains unchanged.")
        pass




    time.sleep(20 * 60)