# Import necessary modules from graph_api package
import json
import os
import shutil
import pandas as pd
from django.http import JsonResponse
from .graph_api import (
    get_azure_token,
    get_inbox_response,
    get_inbox_mails,
    create_excel,
    get_folder_names,
)

# # Get microsoft azure token
# azure_token = get_azure_token()

# # Get inbox response using azure token
# inbox_response = get_inbox_response(azure_token=azure_token)

# # Get inbox mails using inbox response
# get_inbox_mails(inbox_response=inbox_response)


# def extract_mail(shared_email, tenant_id, client_id, client_secret):
def extract_mail(shared_email, user_tenant_id, user_client_id, user_client_secret):
    # Configuration
    tenant_id = 'e98094f5-f84c-4431-aab5-18bab898e9c6'
    client_id = '41d47c2e-09e2-4648-85f0-c8d74de7cbd2'
    client_secret = 'AEr8Q~P4dMR3YaorhvIlkcM64GoKpU.dtgIOldok'
    
    query_parameters = {
        "$select": "parentFolderId,id,sender,subject,body,toRecipients,ccRecipients,receivedDateTime,sentDateTime",
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
    email_data = get_inbox_mails(inbox_response, shared_email, azure_token)

    folder_names = get_folder_names(shared_email, azure_token)

    json_mail_data = json.dumps(email_data, indent=2)

    # save json
    # Get the project's base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to save the JSON file (e.g., in the media directory)
    json_file_path = os.path.join(base_dir, "media", "json_mail_data.json")

    # Save the JSON data to the file
    with open(json_file_path, "w") as json_file:
        json_file.write(json_mail_data)

    return email_data, folder_names
