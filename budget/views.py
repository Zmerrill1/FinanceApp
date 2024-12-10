import csv
from django.shortcuts import render
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Transaction

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    # print(row)

                    Transaction.objects.create(
                        date = row['Transaction Date'],
                        description = row['Description'],
                        amount = row['Amount'],
                    )
                
                messages.success(request, 'CSV files uploaded and processed successfully')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

