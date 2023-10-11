import json
from django.shortcuts import render
from .forms import UserForm
from . import main
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
        json_mail_data = main.extract_mail(shared_email,tenant_id,client_id,client_secret)
        json_mail_data = json.dumps(json_mail_data, indent=4)
        print(json_mail_data)
        # Pass the JSON data to the template context
        # context = {'json_mail_data': json_mail_data}
        return render(request, 'emails.html', {'json_mail_data': json_mail_data})
    else:
        form = UserForm()
        return render(request, 'user_input.html', {'form': form})
    
def email_folders(request):
    return render(request, 'email_folders.html')