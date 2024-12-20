import csv
import hashlib
import io
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CSVUploadForm, TransactionForm
from .models import BudgetItem, Transaction, UploadedFile


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%m/%d/%Y").date()


def parse_amount(amount_str):
    """
    Convert a number string to a standard float.
    If it's in the standard format, parse it directly.
    Otherwise assume it uses a European format and normalize.
    """
    try:
        return float(amount_str)
    except ValueError:
        try:
            normalized_str = amount_str.replace(".", "").replace(",", ".")
            return float(normalized_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {amount_str}")


def calculate_file_hash(file) -> str:
    hasher = hashlib.sha256()
    file.seek(0)
    hasher.update(file.read())
    file.seek(0)
    return hasher.hexdigest()


@login_required
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
            file_hash = calculate_file_hash(csv_file)

            if UploadedFile.objects.filter(file_hash=file_hash).exists():
                messages.error(request, "This file has alrady been uploaded.")
                return render(request, "upload.html", {"form": form})

            UploadedFile.objects.create(
                file_name=csv_file.name,
                file_hash=file_hash,
                user=request.user,
            )

            transactions = []

            for row in reader:
                transaction_date = parse_date(row["Transaction Date"])
                amount = parse_amount(row["Amount"])

                transactions.append(
                    Transaction(
                        account=account,
                        date=transaction_date,
                        description=row["Description"],
                        amount=amount,
                    )
                )

            Transaction.objects.bulk_create(transactions)
            messages.success(
                request,
                f"CSV files uploaded and processed {len(transactions)} successfully",
            )

    return render(request, "upload.html", {"form": form})


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()

    return render(request, "add_transaction.html", {"form": form})


@login_required
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


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect("transaction_list")


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    budget_item = BudgetItem.objects.all()

    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        budget_item_id = request.POST.get("budget_item_id")
        if transaction_id and budget_item_id:
            transaction = Transaction.objects.get(id=transaction_id)
            budget_item = BudgetItem.objects.get(id=budget_item_id)
            transaction.budget_item = budget_item
            transaction.save()
            return redirect("transaction_list")

    return render(
        request,
        "transaction_list.html",
        {"transactions": transactions, "budget_item": budget_item},
    )


def dashboard(request):
    recent_transactions = Transaction.objects.order_by("-date")[:5]

    category_spending = (
        Transaction.objects.filter(transaction_type="EXPENSE")
        .values("budget_item")
        .annotate(total_spent=Sum("amount"))
        .order_by("-total_spent")
    )

    result = Transaction.objects.aggregate(
        total_income=Sum(
            Case(
                When(transaction_type="INCOME", then=F("amount")),
                default=Value(0, output_field=DecimalField()),
            ),
            output_field=DecimalField(),
        ),
        total_expenses=Sum(
            Case(
                When(transaction_type="EXPENSE", then=F("amount")),
                default=Value(0, output_field=DecimalField()),
            ),
            output_field=DecimalField(),
        ),
    )
    total_income = result["total_income"] or 0
    total_expenses = result["total_expenses"] or 0

    context = {
        "recent_transactions": recent_transactions,
        "category_spending": category_spending,
        "total_income": total_income,
        "total_expenses": total_expenses,
    }

    return render(request, "dashboard.html", context)
