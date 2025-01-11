from django.contrib import admin

from .models import Account, Budget, BudgetItem, Transaction, UploadedFile


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name", "start_date", "end_date")


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ("budget", "budget_category", "planned_amount", "spent_amount")
    search_fields = ("budget", "budget_category")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "balance", "account_type")
    search_fields = ("name", "account_type")
    autocomplete_fields = ["user"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "transaction_type",
        "account",
        "description",
        "amount",
        "budget_item",
    )
    search_fields = ("date", "transaction_type", "account", "budget_ite ")
    list_filter = ("date", "transaction_type", "account", "budget_item")


@admin.register(UploadedFile)
class UploadedFileAmin(admin.ModelAdmin):
    pass
