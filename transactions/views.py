from typing import cast

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Transaction


class TransactionUploadView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = cast(AbstractBaseUser, request.user)

        file = request.FILES['file']

        if 'file' not in request.FILES or not isinstance(file, UploadedFile):
            return render(request, 'error.html', {'message': 'No file provided'})

        try:
            count = Transaction.objects.process_file(file, user)
            return render(request, 'success.html', {'count': count})
        except Exception as e:
            return render(request, 'errror.html', {'message': e})
