import json
import uuid

import requests
from app.models import Customer
from django.core.management.base import BaseCommand
from django.urls import reverse

from django_partitioned_audit.models import SimpleAuditEntry


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--server-url", default="http://127.0.0.1:8000")

    def handle(self, *args, **options):
        server_url = options["server_url"]

        print(f"server_url={server_url}")
        original_name = str(uuid.uuid4())
        new_name = str(uuid.uuid4())
        customer = Customer.objects.create(name=original_name)
        url = f"{server_url}{reverse('customer/update', args=[customer.pk])}"
        response = requests.post(url, data=dict(name=new_name))
        response.raise_for_status()

        print("Finished. Now checking...")

        # Assert model was created and audit exists
        for audit in SimpleAuditEntry.objects.filter(object_table="app_customer"):
            # FIXME: filter by `id`
            # Before was possible just by `filter(object_pk=customer.pk)`
            print("-" * 120)
            print(f"Audit: {audit}")
            print(f"object_payload: {json.dumps(json.loads(audit.object_payload), indent=4)}")
