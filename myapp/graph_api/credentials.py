tenant_id = "e98094f5-f84c-4431-aab5-18bab898e9c6"
client_id = "41d47c2e-09e2-4648-85f0-c8d74de7cbd2"
client_secret = "AEr8Q~P4dMR3YaorhvIlkcM64GoKpU.dtgIOldok"
shared_folder_email = "altersense.rpa@altersenseltd.onmicrosoft.com"
user_email = "salman@altersenseltd.onmicrosoft.com"

# tenant_id = input('Enter tenant id: ')
# client_id = input('Enter client id: ')
# client_secret = input('Enter client secret: ')
# shared_folder_email = input('Enter shared folder email: ')

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

graph_api_url = f"https://graph.microsoft.com/v1.0/users/{shared_folder_email}/messages"