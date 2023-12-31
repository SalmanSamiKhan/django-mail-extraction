from myapp.models import EmailMessage
import json
from sqlite3 import OperationalError
from django.http import FileResponse
from django.shortcuts import render
import pandas as pd

from myproject import settings
from .forms import UserForm
from . import main
from . import win32
import os

# Create your views here.
# def user_input(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             # Process the form data here
#             shared_email = form.cleaned_data['shared_email']
#             tenant_id = form.cleaned_data['tenant_id']
#             client_id = form.cleaned_data['client_id']
#             client_secret = form.cleaned_data['client_secret']
#             json_mail_data = main.extract_mail(shared_email,tenant_id,client_id,client_secret)
#             json_mail_data = json.dumps(json_mail_data, indent=2)
#             # Pass the JSON data to the template context
#             context = {'json_mail_data': json_mail_data}
#             return render(request, 'emails.html', context)
#     else:
#         form = UserForm()
#         return render(request, 'user_input.html', {'form': form})


def user_input(request):
    if request.method == "POST":
        # Process the form data here
        shared_email = request.POST.get("email")
        tenant_id = request.POST.get("tenant_id")
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")
        data = main.extract_mail(shared_email, tenant_id, client_id, client_secret)
        # win32.get_mails()
        json_mail_data = data[0]
        folder_names = data[1]
        json_mail_data = json.dumps(json_mail_data, indent=2)
        create_mailbox(folder_names)
        # print(json_mail_data)
        # print('&&&&&&&&&&&&&')
        # print(folder_names)
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # df = pd.DataFrame(data[0])
        # excel_path = os.path.join(base_dir, 'media', 'shared_mails.xlsx')
        # df.to_excel(excel_path, index=False)
        # Pass the JSON data to the template context
        # return render(request, 'emails.html', {'json_mail_data': json_mail_data})
        return render(
            request,
            "email_folders.html",
            {"folder_names": folder_names, "json_mail_data": json_mail_data},
        )
    else:
        form = UserForm()
        return render(request, "user_input.html", {"form": form})


def email_folders(request):
    return render(request, "email_folders.html")


def folder_view(request, folder_name):
    # json file path

    # Get the project's base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to save the JSON file (e.g., in the media directory)
    json_file_path = os.path.join(base_dir, "media", "json_mail_data.json")

    # Load the JSON data from the file
    with open(json_file_path, "r") as file:
        mail_data = json.load(file)

    # print(folder_name)

    # for email in mail_data:
    # print(email.get('Folder Name'))

    filtered_emails = [
        email for email in mail_data if email.get("Folder") == folder_name
    ]
    context = {
        "folder_name": folder_name,
        "filtered_emails": filtered_emails,
    }
    return render(request, "folder_view.html", context)


def download_json(request):
    # Define the path to the JSON file in the media directory
    # Get the project's base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to download the JSON file (e.g., in the media directory)
    json_file_path = os.path.join(base_dir, "media", "json_mail_data.json")
    # json_file_path = os.path.join(settings.MEDIA_ROOT, 'json_mail_data.json')

    # Serve the JSON file as a downloadable response
    response = FileResponse(open(json_file_path, "rb"))
    response["Content-Type"] = "application/json"
    response["Content-Disposition"] = f"attachment; filename=json_mail_data.json"
    return response


def create_mailbox(folder_names):
    print(folder_names)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    media_dir = os.path.join(base_dir, "media")

    try:
        unique_folder_names = EmailMessage.objects.values("folder_name").distinct()
        print(unique_folder_names)
        for folder_name in folder_names:
            folder_path = os.path.join(media_dir, folder_name)
            # for folder in unique_folder_names:
            #     folder_name = folder["folder_name"]
            #     folder_path = os.path.join(media_dir, folder_name)

            try:
                # Create the folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Fetch emails from the database for this folder
                emails = EmailMessage.objects.filter(folder_name=folder_name)
                
                ########################## CSV
                
                csv_data = {
                    "MSGID": [],
                    "FROM": [],
                    "TO": [],
                    "CC": [],
                    "SUBJECT": [],
                    "EMAIL BODY": [],
                    "DATE SENT": [],
                    "DATE RECEIVED": [],
                    "PATH": [],
                }
                
                
                for email in emails:
                    email_data = {
                        "msgid": email.msgid,
                        "sent_date": email.sent_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "received_date": email.received_date.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "from": email.sender,
                        "to": email.receiver,
                        "cc": email.cc,
                        "subject": email.subject,
                        "body": email.body,
                    }
                    
                    ########################## CSV
                    
                    csv_data["MSGID"].append(email.msgid)
                    csv_data["DATE SENT"].append(email.sent_date)
                    csv_data["DATE RECEIVED"].append(email.received_date)
                    csv_data["FROM"].append(email.sender)
                    csv_data["TO"].append(email.receiver)
                    csv_data["CC"].append(email.cc)
                    csv_data["SUBJECT"].append(email.subject)
                    csv_data["EMAIL BODY"].append(email.body)
                    csv_data["PATH"].append(folder_path)

                    # Save the email in JSON format
                    json_file_path = os.path.join(folder_path, f"{email.msgid}.json")
                    pst_file_path = os.path.join(folder_path, f"{email.msgid}.pst")
                    

                    try:
                        # if not os.path.exists(json_file_path):
                        with open(json_file_path, "w") as json_file:
                            json.dump(email_data, json_file, indent=4)
                    except IOError as e:
                        print(f"Error writing JSON file for email {email.msgid}: {e}")
                    
                    try:
                        # if not os.path.exists(json_file_path):
                        with open(pst_file_path, "w") as pst_file:
                            pst_file.write(pst_file)
                    except IOError as e:
                        print(f"Error writing PST file for email {email.msgid}: {e}")

                print(f"%%%%%%$$$$$$$$$$$^^^^^^^^^^^^^\n{csv_data}")
                csv_file_path = os.path.join(folder_path, f"{folder_name}.csv")
                df = pd.DataFrame(csv_data)
                df.to_csv(csv_file_path, index=False)

            except OSError as e:
                print(f"Error creating or accessing folder {folder_name}: {e}")

    except OperationalError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
