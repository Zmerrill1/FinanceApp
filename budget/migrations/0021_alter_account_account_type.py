# Generated by Django 5.1.4 on 2025-01-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0020_alter_account_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("SAVINGS", "Savings"),
                    ("CHECKING", "Checking"),
                    ("CREDIT CARD", "Credit Card"),
                ],
                max_length=50,
            ),
        ),
    ]
