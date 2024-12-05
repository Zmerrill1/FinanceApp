from django.contrib import admin
from .models import Budget
from .models import BudgetItem

admin.site.register(Budget)
admin.site.register(BudgetItem)

