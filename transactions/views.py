from typing import cast

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Transaction


class TransactionUploadView(View):
    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        user = cast(AbstractBaseUser, request.user)

        if 'file' not in request.FILES:
            return render(request, 'transactions/upload/error.html', {'message': 'Geen bestand toegevoegd.'})

        file = request.FILES['file']

        try:
            count = Transaction.objects.process_file(cast(UploadedFile, file), user)
            return render(request, 'transactions/upload/success.html', {'count': count})
        except Exception as e:
            return render(request, 'transactions/upload/error.html', {'message': 'Er is iets overwachts misgegaan.'})
