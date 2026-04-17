import csv
import datetime
from io import TextIOWrapper

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import Model

from typing import Type, TypeVar


T = TypeVar('T', bound=Model)
User = get_user_model()

class TransactionManager[T](models.Manager):
    def process_file(self, file: UploadedFile, user: User) -> int:
        csv_file = TextIOWrapper(file, 'utf-8')
        reader = csv.DictReader(csv_file)
        transactions = []
        for row in reader:
            transaction = self.model(
                date=datetime.date.fromisoformat(row['Datum']),
                user=user,
                amount=float(row['Bedrag'].replace(',', '.')),
                currency=row['Munt'],
                description=(row['Omschrijving-1'] + row['Omschrijving-2'] + row['Omschrijving-3']).strip(),
                follow_number=row['Volgnr'],
                code=row['Code'],
                iban=row['IBAN/BBAN'],
                iban_other_party=row['Tegenrekening IBAN/BBAN'],
                name_other_party=row['Naam tegenpartij'],
            )

            transactions.append(transaction)
        self.model.objects.bulk_create(transactions, ignore_conflicts=True)
        return len(transactions)
