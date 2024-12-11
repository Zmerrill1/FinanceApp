from django import forms
from .models import Transaction

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Upload a CSV file')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description',]