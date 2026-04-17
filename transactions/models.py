from django.contrib.auth import get_user_model
from django.db import models

from .managers import TransactionManager

User = get_user_model()

class Transaction(models.Model):
    objects = TransactionManager()

    follow_number = models.IntegerField(null=False, blank=False)
    iban = models.CharField(null=False, blank=False)
    currency = models.CharField(null=True, blank=True, default='EUR')
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    date = models.DateField(null=False, blank=False)
    name_other_party = models.CharField(null=False, blank=False)
    iban_other_party = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    is_not_fixed = models.BooleanField(default=False)
    code = models.CharField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['iban', 'follow_number', 'user'], name="unique_transaction"
            )
        ]


