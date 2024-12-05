from django.db import models
from category.models import Category
from transactions.models import Transaction

class Budget(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) #total spend amount overall for the budget
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f'{self.name}'

class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2) #not sure why this is giving me an error when I set a default value of 0?

    #adding a relationshop to the Transaction model
    transactions = models.ManyToManyField(Transaction, related_name='budget_items')

    def __str__(self) -> str:
        return f"{self.category.name} - {self.budget.name}"

