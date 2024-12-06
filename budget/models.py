from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length = 50) #i.e, "checking" or "savings" or "credit card", etc.

    def __str__(self) -> str:
        return self.name


class BudgetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Budget(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) #total spend amount overall for the budget
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f'{self.name}'

class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, related_name='items', on_delete=models.CASCADE)
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2) #not sure why this is giving me an error when I set a default value of 0?

    def __str__(self) -> str:
        return f"{self.budget_category.name} - {self.budget.name}"

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
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.amount} ({self.budget_category})"

