

class FollowAndTags:
    def __init__(self, address):
        self.base_url = "https://api.ethfollow.xyz/api/v1/users/"
        self.address = address


    def get_following_url(self):
        endpoint = "/following"
        return f"{self.base_url}{self.address}{endpoint}"
    
    def get_tags_url(self):
        endpoint = "/tags"
        return f"{self.base_url}{self.address}{endpoint}"