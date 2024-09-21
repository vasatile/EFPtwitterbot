class EnsUrl:
    def __init__(self, address):
        self.base_url = "https://api.ethfollow.xyz/api/v1/users/"
        self.address = address

    def get_ens_data_url(self):
        endpoint = "/ens"
        return f"{self.base_url}{self.address}{endpoint}"