from django.db import models
#
# public class Transaction
# {
#     public int Id { get; set; }
#     public int FollowNumber { get; init; }
#     public required string Iban { get; init; }
#     public required string Currency { get; init; }
#     public decimal Amount { get; init; }
#     public DateOnly DateTransaction { get; init; }
#     public decimal BalanceAfterTransaction { get; init; }
#     public string? NameOtherParty { get; init; }
#     public string? IbanOtherParty { get; init; }
#     public string? AuthorizationCode { get; init; }
#     public string? Description { get; init; }
#     public DateOnly? CashbackForDate { get; set; }
#     public string? Code { get; set; }
#     public string? BatchId { get; set; }
#     public string? Reference { get; set; }
#     public required string User { get; init;}
# }

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
    # user = models.ForeignKey()


