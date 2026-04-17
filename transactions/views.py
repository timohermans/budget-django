from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from transactions.models import Transaction


class TransactionUploadView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if 'file' not in request.FILES:
            return render(request, 'error.html', {'message': 'No file provided'})

        file = request.FILES['file']

        try:
            count = Transaction.objects.process_uploaded_file(file)
            return render(request, 'success.html', {'count': count})
        except Exception as e:
            return render(request, 'errror.html', {'message': e})
