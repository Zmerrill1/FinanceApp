from django.contrib import admin
from .models import Budget
from .models import BudgetItem
from .models import Account
from .models import BudgetCategory
from .models import Transaction

admin.site.register(Budget)
admin.site.register(BudgetItem)
admin.site.register(Account)
admin.site.register(BudgetCategory)
admin.site.register(Transaction)
