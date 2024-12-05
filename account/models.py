from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length = 50) #i.e, "checking" or "savings" or "credit card", etc.

    def __str__(self) -> str:
        return self.name
