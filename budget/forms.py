from django import forms

from .models import Account, Transaction


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload a CSV file")
    account = forms.ModelChoiceField(queryset=Account.objects.all())


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ["account", "amount", "date", "description", "budget_item"]
