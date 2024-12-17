from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Account(models.Model):
    ACCOUNT_TYPE = {
        ("CHECKING", "Checking"),
        ("SAVINGS", "Savings"),
        ("CREDIT CARD", "Credit Card"),
    }

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # temporarily making the field nullable.
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)

    def __str__(self) -> str:
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name}"


class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, related_name="items", on_delete=models.CASCADE)
    budget_category = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.budget_category} - {self.budget.name}"


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    description = models.TextField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    budget_item = models.ForeignKey(
        BudgetItem, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.amount} ({self.budget_item})"


class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
        null=True,
        blank=True,
    )  # temporarily making this field nullable

    def __str__(self) -> str:
        user_display = self.user.username if self.user else "Unknown User"
        return f"{self.file_name} uploaded by {user_display}"
