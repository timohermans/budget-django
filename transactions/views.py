from typing import cast

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.http import require_POST

from .models import Transaction
from user.type import User


@require_POST
def toggle_fixed(request):
    id = int(request.POST["id"])
    transaction = get_object_or_404(Transaction, id=id, user=request.user)
    transaction.toggle_fixed()
    return redirect(
        reverse(
            "budget:home",
            kwargs={"year": transaction.date.year, "month": transaction.date.month, "week": transaction.date.isocalendar().week},
        )
    )


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
