import requests
from . import credentials as cred


# class InboxResponse:
def get_inbox_response(azure_token, graph_api_url, query_parameters):
    headers = {
        "Authorization": f"Bearer {azure_token}",
        "Content-Type": "application/json",
    }
    inbox_response = requests.get(
        graph_api_url, params=query_parameters, headers=headers
    )
    # print("Fetch Inbox response success")
    return inbox_response
