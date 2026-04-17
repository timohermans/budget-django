from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.TransactionUploadView.as_view(), name='upload'),
]