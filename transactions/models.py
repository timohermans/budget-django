from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Transaction(models.Model):
    follow_number = models.IntegerField()
    iban = models.CharField()
    currency = models.CharField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    name_other_party = models.CharField()
    iban_other_party = models.CharField()
    authorization_code = models.CharField()
    description = models.TextField()
    is_not_fixed = models.BooleanField()
    code = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


