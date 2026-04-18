from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from transactions.views import TransactionUploadView

# class HomeView(TemplateView):
#     template_name = "myapp/home.html"
#
#     def get_context_data(self, **kwargs):
#         kwargs["environment"] = "Production"
#         return super().get_context_data(**kwargs)

User = get_user_model()

class UploadFileViewTestCase(TestCase):

    @patch('transactions.models.Transaction.objects.process_file')
    def test_post__when_valid_file__calls_manager_and_returns_success(self, mock_process_file: MagicMock):
        mock_process_file.return_value = 10

        request = RequestFactory().post("/")
        request.FILES['file'] = SimpleUploadedFile('transaction.csv', None , 'text/csv')
        request.user = User.objects.create_user('test', '', '')
        view = TransactionUploadView()
        view.setup(request)

        result = view.post(request)

    # context = view.get_context_data()
    # self.assertIn("environment", context)
