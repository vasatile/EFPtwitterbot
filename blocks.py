class Blocks:
    
    def __init__(self, tags_data):
        # Store the tags data passed to the class
        self.tags_data = tags_data
        
    def extract_block_users(self):
        
         # Use .get() to avoid KeyError and specify a default value
        tagged_addresses = self.tags_data.get('taggedAddresses', [])
        if isinstance(tagged_addresses, list):

            # Use self.tags_data to access the instance variable
            all_blocks = [item['address'] for item in tagged_addresses if item.get('tag') == 'block']
            return all_blocks  
        else:
            
            return []  # Return an empty list if the structure is not as expected