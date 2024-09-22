import requests

try:
    response = requests.get('https://api.ethfollow.xyz/api/v1/users/branly.eth/following')
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
