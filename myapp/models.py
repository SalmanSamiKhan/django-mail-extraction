from django.db import models

# Create your models here.

class MailboxCredentials(models.Model):
    shared_mail = models.EmailField()
    tenant_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
