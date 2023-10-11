from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_input, name='user_input'),
    path('emails/', views.user_input, name='user_input'),
    # path('email_folders/', views.email_folders, name='email_folders')
]
