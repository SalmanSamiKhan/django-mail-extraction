from bs4 import BeautifulSoup
import requests
from myapp.models import EmailMessage


# class ExtractInboxMails:
def get_inbox_mails(inbox_response, shared_email, access_token):
    data = []
    if inbox_response.status_code == 200:
        emails = inbox_response.json().get("value", [])
        # print(f'Email Number: {len(emails)}')
        EmailMessage.objects.all().delete()
        for email in emails:
            
            folder_id = email['parentFolderId']
            # Get the folder name using the folder ID
            folder_name = get_folder_name(shared_email, folder_id, access_token)
            
            # Retrieve or create the EmailFolder instance
            # db_folder, _ = EmailFolder.objects.get_or_create(name=folder_name)
            
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
            
            db_receiver_emails = ','.join(receiver_emails)
            db_cc = ','.join(cc_emails)
            # print(folder_name)
            email_msg = EmailMessage(
                folder_name = folder_name,
                msgid = msgid,
                sent_date = sent_time,
                received_date = received_time,
                sender = sender_email,
                receiver = db_receiver_emails,
                cc = db_cc,
                subject = subject,
                body = trimmed_body_text
            )
            
            # Check if the email message already exists in the database
            # existing_message = EmailMessage.objects.filter(msgid=email_msg.msgid).first()
            
            
            email_msg.save()        
    
            

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
