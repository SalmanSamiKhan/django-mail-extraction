from bs4 import BeautifulSoup
import requests


# class ExtractInboxMails:
def get_inbox_mails(inbox_response, shared_email, access_token):
    data = []
    if inbox_response.status_code == 200:
        emails = inbox_response.json().get("value", [])

        for email in emails:
            
            folder_id = email['parentFolderId']
            # Get the folder name using the folder ID
            folder_name = get_folder_name(shared_email, folder_id, access_token)
            
            msgid = email["id"]
            sender = (
                email.get("sender", {})
                .get("emailAddress", {})
                .get("name", "Unknown Sender")
            )
            sender_email = (
                email.get("sender", {})
                .get("emailAddress", {})
                .get("address", "Unknown Address")
            )
            subject = email["subject"]
            body = email.get("body", {}).get("content", "No Content")
            soup = BeautifulSoup(body, "html.parser")
            body_text = soup.get_text()
            # Trim extra spaces from mail body
            trimmed_body_text = " ".join(body_text.split())
            received_time = email["receivedDateTime"]
            sent_time = email["sentDateTime"]

            # Extract receiver information
            to_recipients = email.get("toRecipients", [])
            receiver_names = [
                recipient["emailAddress"]["name"] for recipient in to_recipients
            ]
            receiver_emails = [
                recipient["emailAddress"]["address"] for recipient in to_recipients
            ]

            cc_recipients = email.get("ccRecipients", [])
            cc_emails = [
                recipient["emailAddress"]["address"] for recipient in cc_recipients
            ]

            # print(f"MSGID: {msgid}")
            # print(f"Sent Date: {sent_time}")
            # print(f"Received Date: {received_time}")
            # print(f"From: {sender_email}")
            # print(f"To: {', '.join(receiver_emails)}")
            # print(f"CC: {', '.join(cc_emails)}")
            # print(f"Subject: {subject}")
            # print(f"Body: {trimmed_body_text}")
            # # print(f"Receiver Emails: {', '.join(receiver_emails)}")
            # print("=" * 50)
            
            data.append(
                {
                    'Folder':folder_name,
                    'MSGID': msgid,
                    'Sent': sent_time,
                    'Received': received_time,
                    'From': sender_email,
                    'To': receiver_emails,
                    'CC': cc_emails,
                    'Subject': subject,
                    'Body': trimmed_body_text
                }
            )        
    
            

    else:
        print(f"Error: {inbox_response.status_code} - {inbox_response.text}")
        
    return data

def get_folder_name(shared_email, folder_id, access_token):
    folder_url = f"https://graph.microsoft.com/v1.0/users/{shared_email}/mailFolders/{folder_id}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    folder_response = requests.get(folder_url, headers=headers)
    
    # if folder_response.status_code == 200:
    folder_data = folder_response.json()
    folder_name = folder_data['displayName']
    return folder_name
    # else:
    #     return "Unknown Folder"
