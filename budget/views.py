import csv
import io
from datetime import date, datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

# from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm, TransactionForm
from .models import Transaction


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%m/%d/%Y").date()


# @login_required
def upload_csv(request):
    form = CSVUploadForm()
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            account = form.cleaned_data["account"]

            csv_data = csv_file.read().decode("utf-8")
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string, delimiter=",")

            # existing_transactions = Transaction.objects.filter(
            #     account=account
            # ).select_related("account")

            existing_transactions = {
                (transaction[0], transaction[1], str(transaction[2]))
                for transaction in Transaction.objects.filter(
                    account=account
                ).values_list("date", "description", "amount")
            }
            transactions = []

            for row in reader:
                transaction_date = parse_date(row["Transaction Date"])
                transaction_identifier = (
                    transaction_date,
                    row["Description"],
                    row["Amount"],
                )

                if transaction_identifier in existing_transactions:
                    continue
                transactions.append(
                    Transaction(
                        account=account,
                        date=transaction_date,
                        description=row["Description"],
                        amount=row["Amount"],
                    )
                )
                existing_transactions.add(transaction_identifier)

            Transaction.objects.bulk_create(transactions)
            messages.success(
                request,
                f"CSV files uploaded and processed {len(transactions)} successfully",
            )

    return render(request, "upload.html", {"form": form})


def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()

    return render(request, "add_transaction.html", {"form": form})


def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)

    return render(
        request, "edit_transaction.html", {"form": form, "transaction": transaction}
    )


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect("transaction_list")


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, "transaction_list.html", {"transactions": transactions})
