from typing import cast

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import Transaction
from user.type import User


class TransactionUploadView(View):
    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        user = cast(User, request.user)

        if "file" not in request.FILES:
            return render(
                request,
                "transactions/upload/error.html",
                {"message": "Geen bestand toegevoegd."},
            )

        file = request.FILES["file"]

        try:
            date = Transaction.objects.process_file(cast(UploadedFile, file), user)
            # TODO: logging!
            return redirect(
                reverse(
                    "budget:overview", kwargs={"year": date.year, "month": date.month}
                )
            )
        except Exception as e:
            # TODO: logging!
            return render(
                request,
                "transactions/upload/error.html",
                {"message": "Er is iets overwachts misgegaan."},
            )
