from django.db import models
from account.models import Account
from category.models import Category

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    description = models.TextField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.amount} ({self.category})"