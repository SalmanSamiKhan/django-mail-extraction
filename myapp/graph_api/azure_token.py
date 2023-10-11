import requests
from . import credentials as cred


def get_azure_token(token_url,token_data):
    # Send the token request
    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code == 200:
        token_info = token_response.json()
        access_token = token_info["access_token"]
        # print("Fetch Azure token success")
        return access_token
        # print(f"Access Token: {access_token}")
    else:
        print(f"Error: {token_response.status_code} - {token_response.text}")
