import csv
import datetime
from io import TextIOWrapper
from typing import TypeVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.files.uploadedfile import UploadedFile
from django.db import models

Model = TypeVar("Model", bound=models.Model)


class TransactionManager(models.Manager):
    def process_file(self, uploaded_file: UploadedFile, user: AbstractBaseUser) -> int:
        if uploaded_file.file is None:
            raise ValueError("Uploaded file is not available")
        csv_file = TextIOWrapper(uploaded_file.file, "utf-8")
        reader = csv.DictReader(csv_file)
        transactions = []
        for row in reader:
            transaction = self.model(
                date=datetime.date.fromisoformat(row["Datum"]),
                user=user,
                amount=float(row["Bedrag"].replace(",", ".")),
                currency=row["Munt"],
                description=(
                    row["Omschrijving-1"]
                    + row["Omschrijving-2"]
                    + row["Omschrijving-3"]
                ).strip(),
                follow_number=row["Volgnr"],
                code=row["Code"],
                iban=row["IBAN/BBAN"],
                iban_other_party=row["Tegenrekening IBAN/BBAN"],
                name_other_party=row["Naam tegenpartij"],
            )

            transactions.append(transaction)
        self.bulk_create(transactions, ignore_conflicts=True)
        return len(transactions)
