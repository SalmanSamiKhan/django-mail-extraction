from bs4 import BeautifulSoup


# class ExtractInboxMails:
def get_inbox_mails(inbox_response):
    data = []
    if inbox_response.status_code == 200:
        emails = inbox_response.json().get("value", [])

        for email in emails:
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
                    'MSGID': msgid,
                    'Sent Date': sent_time,
                    'Received Date': received_time,
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
