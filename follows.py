import requests

class Follows:
    def __init__(self, fullurl):
        # Store the full URL
        self.fullurl = fullurl
        
    def fetch_following_data(self):
        # Fetch data from the passed URL
        following_response = requests.get(self.fullurl)

        # Raise an error for bad responses
        following_response.raise_for_status()

        # Parse JSON response
        following_data = following_response.json()
        return following_data

    def extract_addresses(self):
        # Fetch the following data
        following_data = self.fetch_following_data()

        # Extract all addresses
        addresses = [item['address'] for item in following_data['following']]
        return addresses
    
    
    
    def fetch_tags_data(self): 
        
        try: 
        # Fetch data from the passed URL
            tags_response = requests.get(self.fullurl)

            # Raise an error for bad responses
            tags_response.raise_for_status()
            if tags_response.json().get('response') == "Primary List Not Found":
                    return {} 
            # Parse JSON response
            tags_data = tags_response.json()
            return tags_data
        except requests.exceptions.HTTPError:
            return{}
        

    def extract_tags(self):
        # Fetch the following data
        tags_data = self.fetch_tags_data()

        # Extract all tags
        AllTags = tags_data
        return AllTags