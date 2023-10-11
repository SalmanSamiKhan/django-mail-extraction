import requests

def get_folder_names(shared_email, access_token):
    folder_names = []
    
    folder_url = f"https://graph.microsoft.com/v1.0/users/{shared_email}/mailFolders"

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    while folder_url:
        folder_response = requests.get(folder_url, headers=headers)

        if folder_response.status_code == 200:
            folder_data = folder_response.json().get("value", [])

            for folder in folder_data:
                folder_name = folder.get("displayName", "Unknown Folder")
                folder_names.append(folder_name)

            # Check for the presence of nextLink to fetch the next batch of folders
            if '@odata.nextLink' in folder_response.json():
                folder_url = folder_response.json()['@odata.nextLink']
            else:
                break
        else:
            print(f'Failed to retrieve folder list: {folder_response.status_code} - {folder_response.text}')
            break

    return folder_names
