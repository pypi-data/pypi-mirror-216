from app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customer/create/", views.CustomerCreate.as_view(), name="customer/create"),
    path("customer/<int:pk>/update/", views.CustomerUpdate.as_view(), name="customer/update"),
    path("customer/<int:pk>/delete/", views.CustomerDelete.as_view(), name="customer/delete"),
    path("invoice/create/", views.InvoiceCreate.as_view(), name="invoice/create"),
    path("product/create/", views.ProductCreate.as_view(), name="product/create"),
]
