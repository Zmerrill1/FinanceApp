from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("list/", views.transaction_list, name="transaction_list"),
    path("add/", views.add_transaction, name="add_transaction"),
    path("edit/<int:transaction_id>/", views.edit_transaction, name="edit_transaction"),
    path(
        "delete/<int:transaction_id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path("upload/", views.upload_csv, name="upload_csv"),
    path("bankaccounts/", views.bank_account_list, name="bank_account_list"),
    path("bankaccounts/add/", views.add_bank_account, name="add_bank_account"),
    path(
        "bankaccounts/edit/<int:account_id>/",
        views.edit_bank_account,
        name="edit_bank_account",
    ),
    path(
        "bankaccounts/delete/<int:account_id>",
        views.delete_bank_account,
        name="delete_bank_account",
    ),
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/add/", views.add_budget, name="add_budget"),
    path("budgetitem/", views.budget_item_list, name="budget_item_list"),
    path("budgetitem/add/", views.add_budget_item, name="add_budget_item"),
    path(
        "budgetitem/edit/<int:budget_item_id>/",
        views.edit_budget_item,
        name="edit_budget_item",
    ),
    path(
        "budgetitem/delete/<int:budget_item_id>",
        views.delete_budget_item,
        name="delete_budget_item",
    ),
    path("accounts/", include("allauth.urls")),
]
