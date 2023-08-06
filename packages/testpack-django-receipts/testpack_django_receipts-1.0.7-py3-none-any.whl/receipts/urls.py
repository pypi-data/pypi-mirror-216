from django.urls import path
from receipts import views

app_name = "receipts"
urlpatterns = [
    path("receipt_json/", views.receipt_json),
]