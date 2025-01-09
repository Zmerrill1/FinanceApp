# Generated by Django 5.1.4 on 2025-01-09 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0010_alter_account_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("CHECKING", "Checking"),
                    ("CREDIT CARD", "Credit Card"),
                    ("SAVINGS", "Savings"),
                ],
                max_length=50,
            ),
        ),
    ]
