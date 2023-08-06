import time

from app.models import Customer
from app.models import Invoice
from app.models import Product
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView


class CustomerCreate(CreateView):
    success_url = reverse_lazy("customer/create")
    model = Customer
    fields = "__all__"


class CustomerUpdate(UpdateView):
    success_url = reverse_lazy("customer/create")
    model = Customer
    fields = "__all__"

    def post(self, request: HttpRequest, *args, **kwargs):
        pre_wait_ms = int(request.GET.get("pre-wait-ms", "0"))
        post_wait_ms = int(request.GET.get("post-wait-ms", "0"))
        if pre_wait_ms > 0:
            time.sleep(pre_wait_ms / 1000.0)
        response = super().post(request, *args, **kwargs)
        if post_wait_ms > 0:
            time.sleep(post_wait_ms / 1000.0)
        return response


class CustomerDelete(DeleteView):
    success_url = reverse_lazy("customer/create")
    model = Customer
    fields = "__all__"


class InvoiceCreate(CreateView):
    success_url = reverse_lazy("invoice/create")
    model = Invoice
    fields = "__all__"


class ProductCreate(CreateView):
    success_url = reverse_lazy("product/create")
    model = Product
    fields = "__all__"
