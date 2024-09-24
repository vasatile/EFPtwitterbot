import requests
import time

class Follows:
    def __init__(self, fullurl):
        # Store the full URL
        self.fullurl = fullurl

    def fetch_following_data(self):
        while True:
            try:
                # Fetch data from the passed URL
                following_response = requests.get(self.fullurl)

                # Raise an error for bad responses
                following_response.raise_for_status()

                # Parse JSON response
                following_data = following_response.json()
                return following_data

            except requests.exceptions.ConnectionError:
                print("Connection error occurred. Retrying in 30 minutes...")
                time.sleep(30 * 60)  # Wait for 30 minutes
            except requests.exceptions.Timeout:
                print("Request timed out. Retrying in 30 minutes...")
                time.sleep(30 * 60)  # Wait for 30 minutes
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return {}
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return {}

    def extract_addresses(self):
        # Fetch the following data
        following_data = self.fetch_following_data()

        # Extract all addresses, return empty list if no data
        addresses = [item['address'] for item in following_data.get('following', [])]
        return addresses

    def fetch_tags_data(self):
        while True:
            try:
                # Fetch data from the passed URL
                tags_response = requests.get(self.fullurl)

                # Raise an error for bad responses
                tags_response.raise_for_status()

                # Check if the response indicates a missing primary list
                if tags_response.json().get('response') == "Primary List Not Found":
                    return {}

                # Parse JSON response
                tags_data = tags_response.json()
                return tags_data

            except requests.exceptions.ConnectionError:
                print("Connection error occurred. Retrying in 30 minutes...")
                time.sleep(30 * 60)  # Wait for 30 minutes
            except requests.exceptions.Timeout:
                print("Request timed out. Retrying in 30 minutes...")
                time.sleep(30 * 60)  # Wait for 30 minutes
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return {}
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return {}

    def extract_tags(self):
        # Fetch the tags data
        tags_data = self.fetch_tags_data()

        # Extract all tags, return empty dict if no data
        all_tags = tags_data if tags_data else {}
        return all_tags
