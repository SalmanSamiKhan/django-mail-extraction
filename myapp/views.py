import json
from django.shortcuts import render
from .forms import UserForm
from . import main
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
    if request.method == 'POST':
        # Process the form data here
        shared_email = request.POST.get('email')
        tenant_id = request.POST.get('tenant_id')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        data = main.extract_mail(shared_email,tenant_id,client_id,client_secret)
        json_mail_data = data[0]
        folder_names = data[1]
        json_mail_data = json.dumps(json_mail_data, indent=2)
        print(json_mail_data)
        print('&&&&&&&&&&&&&')
        print(folder_names)
        # Pass the JSON data to the template context
        # return render(request, 'emails.html', {'json_mail_data': json_mail_data})
        return render(request, 'email_folders.html', {'folder_names':folder_names, 'json_mail_data':json_mail_data})
    else:
        form = UserForm()
        return render(request, 'user_input.html', {'form': form})
    
def email_folders(request):
    return render(request, 'email_folders.html')





def folder_view(request, folder_name):
    
    # json file path

    # Get the project's base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to save the JSON file (e.g., in the media directory)
    json_file_path = os.path.join(base_dir, 'media', 'json_mail_data.json')

    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        mail_data = json.load(file)
    
    print(folder_name)
    
    for email in mail_data:
        print(email.get('Folder Name'))
    
    filtered_emails = [email for email in mail_data if email.get('Folder') == folder_name]
    context = {
        'folder_name': folder_name,
        'filtered_emails': filtered_emails,
    }
    return render(request, 'folder_view.html', context)