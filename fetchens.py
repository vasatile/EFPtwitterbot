import requests

class FetchEns:
    
    def __init__(self, fullurl):
        # Store the full URL
        self.fullurl = fullurl
        
    def fetch_ens_data(self):
        try:
            # Fetch data from the passed URL with a timeout
            ens_response = requests.get(self.fullurl, timeout=60)  # 60 seconds timeout
            # Raise an error for bad responses
            ens_response.raise_for_status()
            # Parse JSON response
            ens_data = ens_response.json()
            return ens_data

        except requests.Timeout:
            # Handle timeout exception
            print(f"Request timed out for URL: {self.fullurl}")
            return None
        except requests.RequestException as e:
            # Handle other possible exceptions
            print(f"Request failed for URL: {self.fullurl}: {e}")
            return None


    def extract_ens(self):
        # Fetch the following data
        ens_data = self.fetch_ens_data()

        if ens_data:
            # ens extract
            name = ens_data.get("ens", {}).get("name", "")
            return name
        return ""


    def extract_xtag(self):
        
        # Fetch ENS data
            xtag_data = self.fetch_ens_data()

            if xtag_data:
                # Fetch the ENS section
                ens_section = xtag_data.get("ens", {})
                
                # Fetch the 'records' section and ensure it's not None
                records = ens_section.get("records")
                if records:
                    # Fetch the Twitter handle from the 'records' dictionary if it exists
                    xtag_name = records.get("com.twitter", "")
                    return xtag_name
                else:
                    # Handle the case where 'records' is None
                    print(f"Records are missing or None for ENS data: {ens_section.get('address')}")
                    return ""

            return ""  # Return empty string if no data
