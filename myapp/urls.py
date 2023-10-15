from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_input, name='user_input'),
    path('emails/', views.user_input, name='user_input'),
    path('email_folders/', views.user_input, name='email_folders'),
    path('folder/<str:folder_name>/', views.folder_view, name='folder_view'),
    path('download_json/', views.download_json, name='download_json'),
]
