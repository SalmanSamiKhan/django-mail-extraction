from django.db import models

# Create your models here.

# class EmailFolder(models.Model):
#     name = models.CharField(max_length=255)
    
class EmailMessage(models.Model):
    # folder = models.ForeignKey(EmailFolder, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255)
    msgid = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    sender = models.EmailField()
    receiver = models.TextField()  # Store recipients as a comma-separated string
    cc = models.TextField()  # Store CC as a comma-separated string
    subject = models.CharField(max_length=255)
    body = models.TextField()
