import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
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

            csv_data = csv_file.read().decode('utf-8')
            io_string = io.StringIO(csv_data)
            reader = csv.DictReader(io_string, delimiter=';')

            transactions = []
            for row in reader:
                   transactions.append(Transaction(
                          account = row['Account'], #Account probably wouldn't be listed on the csv, since the file will come from a single CSV file. But would be the same for each item in a CSV upload
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
               form.save()
               return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})

def edit_transaction(request, transaction_id): #would the database automatically generate a transaction_id or do I need to add that do the model?
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