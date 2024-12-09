from django.contrib import admin
from .models import Budget
from .models import BudgetItem
from .models import Account
from .models import BudgetCategory
from .models import Transaction

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_amount', 'start_date', 'end_date')
    search_fields = ('name', 'total_amount')

@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('budget', 'budget_category', 'planned_amount', 'spent_amount')
    search_fields = ('budget', 'budget_category')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'account_type')
    search_fields = ('name', 'account_type')
    autocomplete_fields = ['user']

@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'transaction_type', 'account', 'description', 'amount', 'budget_category')
    search_fields = ('date', 'transaction_type', 'account', 'budget_category')
    list_filter = ('date', 'transaction_type', 'account', 'budget_category')
