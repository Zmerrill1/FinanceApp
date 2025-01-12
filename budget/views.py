import csv
import hashlib
import io
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, DecimalField, F, Q, Sum, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware

from .forms import (
    AccountForm,
    BudgetForm,
    BudgetItemForm,
    CSVUploadForm,
    TransactionForm,
)
from .models import Account, Budget, BudgetItem, Transaction, UploadedFile


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


def save_transactions(transactions):
    """
    Save a list of Transaction objects to the database.
    """
    Transaction.objects.bulk_create(transactions)


def parse_transaction_row(
    row, account, date_column, amount_column, description_column, header=True
):
    """
    Parse a row and return a Transaction object, or None if invalid.
    """
    try:
        if header:
            transaction_date = parse_date(row[date_column])
            amount = parse_amount(row[amount_column])
            description = row[description_column]
        else:
            transaction_date = parse_date(row[int(date_column)])
            amount = parse_amount(row[int(amount_column)])
            description = row[int(description_column)]

        transaction_type = "EXPENSE" if amount < 0 else "INCOME"
        amount = abs(amount)

        return Transaction(
            account=account,
            date=transaction_date,
            description=description,
            amount=amount,
            transaction_type=transaction_type,
        )
    except (ValueError, KeyError, IndexError):
        # Log or handle parsing errors as needed
        return None


def process_csv_file(csv_file, account, date_column, amount_column, description_column):
    """
    Process CSV file and return a list of Transaction objects.
    """
    csv_file.seek(0)

    csv_data = csv_file.read(512).decode("utf-8")
    io_string = io.StringIO(csv_data)

    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(csv_data).delimiter
    csv_file.seek(0)

    transactions = []
    has_header = sniffer.has_header(csv_data)

    if has_header:
        reader = csv.DictReader(io_string, delimiter=delimiter)
        for row in reader:
            transaction = parse_transaction_row(
                row, account, "Transaction Date", "Amount", "Description"
            )
            if transaction:
                transactions.append(transaction)
    else:
        reader = csv.reader(io_string, delimiter=",")
        for row in reader:
            try:
                transaction = parse_transaction_row(
                    row,
                    account,
                    date_column,
                    amount_column,
                    description_column,
                    header=False,
                )
                if transaction:
                    transactions.append(transaction)
            except IndexError:
                continue  # Skip rows with insufficient columns

    return transactions, has_header


def detect_csv_header(csv_file):
    sniffer = csv.Sniffer()
    csv_data = csv_file.read(512).decode("utf-8")
    has_header = sniffer.has_header(csv_data)
    csv_file.seek(0)
    return has_header


@login_required
def upload_csv(request):
    form = CSVUploadForm()

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Extract form data
            csv_file = request.FILES["file"]
            account = form.cleaned_data["account"]
            has_header = form.cleaned_data["has_header"]
            date_column = form.cleaned_data["date_column"]
            amount_column = form.cleaned_data["amount_column"]
            description_column = form.cleaned_data["description_column"]

            # has_header = detect_csv_header(csv_file)

            # If no header is detected, we proceed to handle the indices
            if not has_header:
                if date_column and amount_column and description_column:
                    # Process the CSV data using the user-specified column indices
                    transactions, _ = process_csv_file(
                        csv_file,
                        account,
                        date_column,
                        amount_column,
                        description_column,
                    )
                    save_transactions(transactions)
                    messages.success(
                        request,
                        f"CSV file uploaded and {len(transactions)} transactions processed successfully.",
                    )
                    # Treat the file as having headers now after processing with indices
                    has_header = True  # Set to True as we are processing the file now with indices
                    return render(
                        request, "upload.html", {"form": form, "has_header": False}
                    )

                else:
                    # If no indices are provided, ask for the column indices
                    messages.warning(
                        request,
                        "No headers detected in your CSV file. Please specify the column indices.",
                    )
                    return render(
                        request, "upload.html", {"form": form, "has_header": False}
                    )

            else:
                # If headers exist, proceed with checking for duplicates and processing
                file_hash = calculate_file_hash(csv_file)
                if UploadedFile.objects.filter(file_hash=file_hash).exists():
                    messages.error(request, "This file has already been uploaded.")
                    return render(
                        request, "upload.html", {"form": form, "has_header": True}
                    )

                # Save uploaded file metadata
                UploadedFile.objects.create(
                    file_name=csv_file.name,
                    file_hash=file_hash,
                    user=request.user,
                )

                try:
                    # Process the CSV data if headers are detected
                    transactions, _ = process_csv_file(
                        csv_file,
                        account,
                        date_column,
                        amount_column,
                        description_column,
                    )
                    save_transactions(transactions)
                    messages.success(
                        request,
                        f"CSV file uploaded and {len(transactions)} transactions processed successfully.",
                    )
                    return render(
                        request, "upload.html", {"form": form, "has_header": True}
                    )

                except Exception as e:
                    messages.error(request, f"Error processing CSV: {e}")

    return render(request, "upload.html", {"form": form, "has_header": False})


# def upload_csv(request):
#     form = CSVUploadForm()

#     if request.method == "POST":
#         form = CSVUploadForm(request.POST, request.FILES)

#         if form.is_valid():
#             # Extract form data
#             csv_file = request.FILES["file"]
#             account = form.cleaned_data["account"]
#             date_column = form.cleaned_data["date_column"]
#             amount_column = form.cleaned_data["amount_column"]
#             description_column = form.cleaned_data["description_column"]

#             has_header = detect_csv_header(csv_file)

#             if not has_header:
#                 if date_column and amount_column and description_column:
#                     transactions, _ = process_csv_file(
#                     csv_file, account, date_column, amount_column, description_column
#                 )
#                     save_transactions(transactions)
#                     messages.success(
#                         request,
#                         f"CSV file uploaded and {len(transactions)} transactions processed successfully.",
#                     )
#                     has_header = True
#                     return render(request, "upload.html", {"form": form, "has_header": has_header})
#                 else:
#                     #no header detected and no indices provided, ask for the column indices
#                     messages.warning(request, "No headers detected in your CSV file. Please specify the column indices.")
#                     return render(request, "upload.html", {"form": form, "has_header": "false"})

#             # Calculate hash and check for duplicates
#             file_hash = calculate_file_hash(csv_file)
#             if UploadedFile.objects.filter(file_hash=file_hash).exists():
#                 messages.error(request, "This file has already been uploaded.")
#                 return render(request, "upload.html", {"form": form, "has_header": "false"})

#             # Save uploaded file metadata
#             UploadedFile.objects.create(
#                 file_name=csv_file.name,
#                 file_hash=file_hash,
#                 user=request.user,
#             )

#             try:
#                 #Process the CSV data based on whether it has a heade
#                 transactions, _ = process_csv_file(
#                 csv_file, account, date_column, amount_column, description_column
#             )
#                 save_transactions(transactions)
#                 messages.success(
#                     request,
#                     f"CSV file uploaded and {len(transactions)} transactions processed successfully.",
#                 )

#                 return render(request, "upload.html", {"form": form, "has_header": has_header})

#             except Exception as e:
#                 messages.error(request, f"Error processing CSV: {e}")

#     return render(request, "upload.html", {"form": form, "has_header": "false"})


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
    today = datetime.today()
    filter_option = request.GET.get("filter", "this_month")
    start_date, end_date = get_date_range(filter_option, request, today)

    date_filter = Q()
    if start_date and end_date:
        date_filter = Q(date__range=(start_date, end_date))

    transactions = Transaction.objects.all().filter(date_filter).order_by("-date")
    budget_items = BudgetItem.objects.all()

    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        budget_item_id = request.POST.get("budget_item_id")
        if transaction_id and budget_item_id:
            transaction = Transaction.objects.get(id=transaction_id)
            budget_item: BudgetItem = BudgetItem.objects.get(id=budget_item_id)
            transaction.budget_item = budget_item
            transaction.save()
            return redirect("transaction_list")

    return render(
        request,
        "transaction_list.html",
        {
            "transactions": transactions,
            "budget_items": budget_items,
            "filter_option": filter_option,
        },
    )


def create_date_range(filter_option, today):
    match filter_option:
        case "this_month":
            start_date = today.replace(day=1)
            end_date = today
        case "last_month":
            first_of_this_month = today.replace(day=1)
            start_date = (first_of_this_month - timedelta(days=1)).replace(day=1)
            end_date = first_of_this_month - timedelta(days=1)
        case "this_year":
            start_date = today.replace(month=1, day=1)
            end_date = today
        case "last_year":
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = today.replace(year=today.year - 1, month=12, day=31)
        case _:
            start_date, end_date = None, None
    return start_date, end_date


def validate_custom_dates(request):
    """Parses and validates the custom dates from the request."""
    try:
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            raise ValueError(
                "Start date and end date are required for the custom filter"
            )

        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))

        if start_date > end_date:
            raise ValueError("Start date cannot be later than end date.")
    except (ValueError, TypeError) as e:
        print(f"Invalid custom date range: {e}")
        start_date, end_date = None, None
    return start_date, end_date


def get_date_range(filter_option, request, today):
    if filter_option == "custom":
        return validate_custom_dates(request)
    else:
        return create_date_range(filter_option, today)


@login_required
def dashboard(request):
    today = datetime.today()
    filter_option = request.GET.get("filter", "this_month")
    start_date, end_date = get_date_range(filter_option, request, today)

    date_filter = Q()
    if start_date and end_date:
        date_filter = Q(date__range=(start_date, end_date))

    recent_transactions = (
        Transaction.objects.select_related("budget_item")
        .filter(date_filter)
        .order_by("-date")[:5]
    )

    category_spending = (
        Transaction.objects.filter(date_filter, transaction_type="EXPENSE")
        .values("budget_item__budget_category")
        .annotate(total_spent=Sum("amount"))
        .order_by("budget_item__budget_category")
    )

    result = Transaction.objects.filter(date_filter).aggregate(
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
        "filter_option": filter_option,
    }

    return render(request, "dashboard.html", context)


@login_required
def bank_account_list(request):
    accounts = Account.objects.all()
    return render(request, "bank_account_list.html", {"accounts": accounts})


@login_required
def add_bank_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bank_account_list")
    else:
        form = AccountForm()
    return render(request, "add_bank_account.html", {"form": form})


@login_required
def edit_bank_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("bank_account_list")
    else:
        form = AccountForm(instance=account)
    return render(request, "edit_bank_account.html", {"form": form, "account": account})


@login_required
def delete_bank_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        account.delete()
        return redirect("bank_account_list")
    return render(request, "delete_bank_account.html", {"account": account})


@login_required
def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, "budget_list.html", {"budgets": budgets})


@login_required
def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("budget_list")
        else:
            return render(request, "add_budget.html", {"form": form})
    else:
        form = BudgetForm()
    return render(request, "add_budget.html", {"form": form})


@login_required
def budget_item_list(request):
    budget_items = BudgetItem.objects.all()
    return render(request, "budget_item_list.html", {"budget_items": budget_items})


@login_required
def add_budget_item(request):
    if request.method == "POST":
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("budget_item_list")
    else:
        form = BudgetItemForm()
    return render(request, "add_budget_item.html", {"form": form})


@login_required
def edit_budget_item(request, budget_item_id):
    item = get_object_or_404(BudgetItem, id=budget_item_id)
    if request.method == "POST":
        form = BudgetItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("budget_item_list")
    else:
        form = BudgetItemForm(instance=item)
    return render(request, "edit_budget_item.html", {"form": form})


@login_required
def delete_budget_item(request, budget_item_id):
    item = get_object_or_404(BudgetItem, id=budget_item_id)
    item.delete()
    return redirect("budget_item_list")
