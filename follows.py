import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Follows:
    def __init__(self, fullurl):
        # Store the full URL
        self.fullurl = fullurl

    def fetch_following_data(self):
        try:
            # Fetch data from the passed URL
            following_response = requests.get(self.fullurl, timeout=10)  # Add a timeout parameter

            # Raise an error for bad responses
            following_response.raise_for_status()

            # Parse JSON response
            following_data = following_response.json()
            return following_data

        except requests.exceptions.ConnectionError:
            logging.error("Connection error occurred. Exiting fetch_following_data.")
            return None  # Return None to indicate failure
        except requests.exceptions.Timeout:
            logging.error("Request timed out. Exiting fetch_following_data.")
            return None  # Return None to indicate failure
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return None  # Return None to indicate failure
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
            return None  # Return None to indicate failure

    def extract_addresses(self):
        # Fetch the following data
        following_data = self.fetch_following_data()

        if following_data is not None:
            # Extract all addresses, return empty list if no data
            addresses = [item['address'] for item in following_data.get('following', [])]
            return addresses
        else:
            return []  # Return an empty list if fetching failed

    def fetch_tags_data(self):
        try:
            # Fetch data from the passed URL
            tags_response = requests.get(self.fullurl, timeout=10)  # Add a timeout parameter

            # Raise an error for bad responses
            tags_response.raise_for_status()

            # Check if the response indicates a missing primary list
            if tags_response.json().get('response') == "Primary List Not Found":
                return {}

            # Parse JSON response
            tags_data = tags_response.json()
            return tags_data

        except requests.exceptions.ConnectionError:
            logging.error("Connection error occurred. Exiting fetch_tags_data.")
            return None  # Return None to indicate failure
        except requests.exceptions.Timeout:
            logging.error("Request timed out. Exiting fetch_tags_data.")
            return None  # Return None to indicate failure
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return None  # Return None to indicate failure
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
            return None  # Return None to indicate failure

    def extract_tags(self):
        # Fetch the tags data
        tags_data = self.fetch_tags_data()

        if tags_data is not None:
            # Extract all tags, return empty dict if no data
            all_tags = tags_data if tags_data else {}
            return all_tags
        else:
            return {}  # Return an empty dict if fetching failed
