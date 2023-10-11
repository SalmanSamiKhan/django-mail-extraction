from django import forms

class UserForm(forms.Form):
    shared_email = forms.EmailField(label='Shared Email')
    tenant_id = forms.CharField(label='Tenant Id')
    client_id = forms.CharField(label='Client Id')
    client_secret = forms.CharField(label='Client Secret')
    
