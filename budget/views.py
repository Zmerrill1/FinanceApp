import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm, TransactionForm
from .models import Transaction

# @login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            account = form.cleaned_data['account']

            csv_data = csv_file.read().decode('utf-8')
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string, delimiter=';')

            transactions = []
            for row in reader:
                   existing_transactions = Transaction.objects.filter(
                        date=row['Transaction Date'],
                        description = row['Description'],
                        amount = row['Amount']
                   ).exists()

                   if not existing_transactions:
                    transactions.append(Transaction(
                            account = account, #this seems weird to have two instances of account. maybe move the form.cleaned_data['account] to here to avoid the redundancy?
                            date = row['Transaction Date'],
                            description = row['Description'],
                            amount = row['Amount'],
                    ))

            Transaction.objects.bulk_create(transactions)
            messages.success(request, f'CSV files uploaded and processed {len(transactions)} successfully')
    
    return render(request, 'upload.html', {'form': form}) 

def add_transaction(request):
    if request.method == 'POST':
          form = TransactionForm(request.POST)
          
          if form.is_valid():
               account = form.cleaned_data['account']
               form.save()
               return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id =transaction_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
         form = TransactionForm(instance=transaction)
          
    return render(request, 'edit_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction(request, transaction_id):
     transaction = get_object_or_404(Transaction, id=transaction_id)
     transaction.delete()
     return redirect('transaction_list')

def transaction_list(request):
     transactions = Transaction.objects.all()
     return render(request, 'transaction_list.html', {'transactions': transactions})