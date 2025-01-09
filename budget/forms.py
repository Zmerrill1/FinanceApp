from django import forms

from .models import Account, Budget, BudgetItem, Transaction


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload a CSV file")
    account = forms.ModelChoiceField(queryset=Account.objects.all())


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = [
            "account",
            "amount",
            "date",
            "description",
            "budget_item",
            "transaction_type",
        ]


class TransactionBudgetItemForm(forms.Form):
    budget_item = forms.ModelChoiceField(
        queryset=BudgetItem.objects.all(), empty_label="Select Budget Item"
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "balance", "account_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "balance": forms.NumberInput(
                attrs={"class": "border rounded px-4 py-2 w-full"}
            ),
            "account_type": forms.Select(
                attrs={"class": "border rounded px-4 py-2 w-full"}
            ),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["name", "start_date", "end_date"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name is None or name.strip() == "":
            raise forms.ValidationError("The budget name cannot be empty.")

        name = name.strip()

        if Budget.objects.filter(name=name).exists():
            raise forms.ValidationError("A budget with this name already exists.")

        return name


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = [
            "budget",
            "budget_category",
            "description",
            "planned_amount",
            "spent_amount",
        ]

    budget = forms.ModelChoiceField(
        queryset=Budget.objects.all(),
        empty_label="Select a budget",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            }
        ),
    )
