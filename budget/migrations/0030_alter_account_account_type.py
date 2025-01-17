# Generated by Django 5.1.4 on 2025-01-14 01:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0029_alter_account_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("SAVINGS", "Savings"),
                    ("CREDIT CARD", "Credit Card"),
                    ("CHECKING", "Checking"),
                ],
                max_length=50,
            ),
        ),
    ]
