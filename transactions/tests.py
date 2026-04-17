import datetime
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from transactions.models import Transaction

User = get_user_model()


class TransactionManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test', email='', password='')

    @staticmethod
    def _to_uploaded_file(csv_string: str):
        csv_data = StringIO(csv_string.strip())
        mock_file = SimpleUploadedFile(
            "test_transactions.csv",
            csv_data.read().encode(),
            content_type="text/csv"
        )
        return mock_file

    def test_process_file__when_only_header__succeeds(self):
        user = User.objects.get(username='test')
        mock_file = self._to_uploaded_file("""
"IBAN/BBAN","Munt","BIC","Volgnr","Datum","Rentedatum","Bedrag","Saldo na trn","Tegenrekening IBAN/BBAN","Naam tegenpartij","Naam uiteindelijke partij","Naam initiÎrende partij","BIC tegenpartij","Code","Batch ID","Transactiereferentie","Machtigingskenmerk","Incassant ID","Betalingskenmerk","Omschrijving-1","Omschrijving-2","Omschrijving-3","Reden retour","Oorspr bedrag","Oorspr munt","Koers"
        """)

        result = Transaction.objects.process_file(mock_file, user)

        self.assertEqual(0, result)
        self.assertEqual(0, len(Transaction.objects.all()))

    def test_process_file__when_single_line__succeeds(self):
        csv_string = """
"IBAN/BBAN","Munt","BIC","Volgnr","Datum","Rentedatum","Bedrag","Saldo na trn","Tegenrekening IBAN/BBAN","Naam tegenpartij","Naam uiteindelijke partij","Naam initiÎrende partij","BIC tegenpartij","Code","Batch ID","Transactiereferentie","Machtigingskenmerk","Incassant ID","Betalingskenmerk","Omschrijving-1","Omschrijving-2","Omschrijving-3","Reden retour","Oorspr bedrag","Oorspr munt","Koers"
"OWNED1","EUR","RABONL2U","000000000000011111","2026-04-15","2026-04-15","-24,66","+5555,27","THEIRS01","Shop","","","RABONLLLXXX","ie","0000000000000000","","","","","Payment"," ","","","","",""
        """
        mock_file = self._to_uploaded_file(csv_string)
        user = User.objects.get(username='test')

        Transaction.objects.process_file(mock_file, user)

        transactions = Transaction.objects.all()
        self.assertEqual(1, len(transactions))
        transaction = transactions[0]
        self.assertEqual('OWNED1', transaction.iban)
        self.assertEqual('EUR', transaction.currency)
        self.assertEqual(datetime.date(2026, 4, 15), transaction.date)
        self.assertEqual(Decimal('-24.66'), transaction.amount)
        self.assertEqual('THEIRS01', transaction.iban_other_party)
        self.assertEqual('Shop', transaction.name_other_party)
        self.assertEqual('ie', transaction.code)
        self.assertEqual('Payment', transaction.description)

    def test_process_file__when_inserting_duplicates__ignores_duplicate(self):
        user = User.objects.get(username='test')
        csv_string = """
"IBAN/BBAN","Munt","BIC","Volgnr","Datum","Rentedatum","Bedrag","Saldo na trn","Tegenrekening IBAN/BBAN","Naam tegenpartij","Naam uiteindelijke partij","Naam initiÎrende partij","BIC tegenpartij","Code","Batch ID","Transactiereferentie","Machtigingskenmerk","Incassant ID","Betalingskenmerk","Omschrijving-1","Omschrijving-2","Omschrijving-3","Reden retour","Oorspr bedrag","Oorspr munt","Koers"
"OWNED1","EUR","RABONL2U","000000000000011111","2026-04-15","2026-04-15","-24,66","+5555,27","THEIRS01","Shop","","","RABONLLLXXX","ie","0000000000000000","","","","","Payment"," ","","","","",""
        """
        file_1 = self._to_uploaded_file(csv_string)
        file_2 = self._to_uploaded_file(csv_string)
        Transaction.objects.process_file(file_1, user)

        # act
        Transaction.objects.process_file(file_2, user)

        self.assertEqual(1, len(Transaction.objects.all()))


class TransactionTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test', email='', password='')

    def test_create__when_user_exists__succeeds(self):
        transaction = Transaction.objects.create(
            follow_number=1,
            iban='OWNED1',
            currency='EUR',
            amount=10,
            date=datetime.date.today(),
            name_other_party='shop',
            iban_other_party='THEIRS1',
            description='TEST',
            user=User.objects.get(username='test'),
            code='ei',
        )

        self.assertIsNotNone(transaction)
