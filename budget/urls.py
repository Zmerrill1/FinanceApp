from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.transaction_list, name="transaction_list"),
    path("add/", views.add_transaction, name="add_transaction"),
    path("edit/<int:transaction_id>/", views.edit_transaction, name="edit_transaction"),
    path(
        "delete/<int:transaction_id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path("upload/", views.upload_csv, name="upload_csv"),
]
