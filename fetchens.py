import requests

class FetchEns:
    def __init__(self, fullurl):
        # Store the full URL
        self.fullurl = fullurl
        
    def fetch_ens_data(self):
        # Fetch data from the passed URL
        ens_response = requests.get(self.fullurl)

        # Raise an error for bad responses
        ens_response.raise_for_status()

        # Parse JSON response
        ens_data = ens_response.json()
        return ens_data

    def extract_ens(self):
        # Fetch the following data
        ens_data = self.fetch_ens_data()

        # ens extract
        name = ens_data["ens"]["name"]
        return name