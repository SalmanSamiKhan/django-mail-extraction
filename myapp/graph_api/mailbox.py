from myapp.models import EmailMessage
import os
import json

def create_mailbox():
    # Fetch unique folder names from the database
    unique_folder_names = EmailMessage.objects.values('folder_name').distinct()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Create a directory for each folder
    media_root = os.path.join(base_dir, 'media')
    mailbox_path = os.path.join(media_root, 'Shared Mailbox')
    print(media_root)
    
    # if not os.path.exists(mailbox_path):
    #     os.mkdir(mailbox_path)