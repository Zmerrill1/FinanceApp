from django import forms

from .models import Account, BudgetItem, Transaction


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload a CSV file")
    account = forms.ModelChoiceField(queryset=Account.objects.all())


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ["account", "amount", "date", "description", "budget_item"]


class TransactionBudgetItemForm(forms.Form):
    budget_item = forms.ModelChoiceField(
        queryset=BudgetItem.objects.all(), empty_label="Select Budget Item"
    )
