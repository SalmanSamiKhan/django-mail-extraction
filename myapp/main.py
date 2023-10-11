# Import necessary modules from graph_api package
import json
from django.http import JsonResponse
from .graph_api import get_azure_token, get_inbox_response, get_inbox_mails, create_excel

# # Get microsoft azure token
# azure_token = get_azure_token()

# # Get inbox response using azure token
# inbox_response = get_inbox_response(azure_token=azure_token)

# # Get inbox mails using inbox response
# get_inbox_mails(inbox_response=inbox_response)


def extract_mail(shared_email,tenant_id,client_id,client_secret):
    
    # Configuration
    query_parameters = {
        "$select": "id,sender,subject,body,toRecipients,ccRecipients,receivedDateTime,sentDateTime",
        "$orderby": "sentDateTime desc",  # Sort by received date/time in descending order
    }

    scopes = [
        "https://graph.microsoft.com/.default"
    ]  # Use the appropriate scope for your needs
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # Prepare the token request data
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "scope": " ".join(scopes),
        "client_secret": client_secret,
    }

    graph_api_url = f"https://graph.microsoft.com/v1.0/users/{shared_email}/messages"
    
    # Get microsoft azure token
    azure_token = get_azure_token(token_url, token_data)

    # Get inbox response using azure token
    inbox_response = get_inbox_response(azure_token, graph_api_url, query_parameters)

    # Get inbox mails using inbox response
    email_data = get_inbox_mails(inbox_response=inbox_response)
    # json_email_data = json.dumps(email_data, indent=2)
    # json_email_data = JsonResponse({'json email data':json_email_data})
    json_email_data = email_data
    return json_email_data
