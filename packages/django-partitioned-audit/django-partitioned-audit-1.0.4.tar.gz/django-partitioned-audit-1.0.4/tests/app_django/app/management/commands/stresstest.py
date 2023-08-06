import itertools
import random
import uuid
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from app.models import Customer
from django.core.management.base import BaseCommand
from django.urls import reverse

from django_partitioned_audit.models import SimpleAuditEntry


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--server-url", default="http://127.0.0.1:8011")
        parser.add_argument("--items", default=10000, type=int)
        parser.add_argument("--max-workers", default=20, type=int)

    def handle(self, *args, **options):
        live_server = options["server_url"]
        items = options["items"]
        max_workers = options["max_workers"]

        print(f"server_url={live_server}")
        print(f"items={items}")
        print(f"max_workers={max_workers}")

        original_name = str(uuid.uuid4())
        customer = Customer.objects.create(name=original_name)
        urls = [
            # Don't wait for most of the requests
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
            # Wait in different ways
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=100&post-wait-ms=0",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=100",
            f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=100&post-wait-ms=100",
        ]
        random.shuffle(urls)

        def _update(url: str, new_name: str):
            response = requests.post(url, data=dict(name=new_name))
            response.raise_for_status()

        new_names = [str(uuid.uuid4()) for _ in range(items)]

        # We can use a with statement to ensure threads are cleaned up promptly
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Start the load operations and mark each future with its URL
            url_iterator = itertools.cycle(urls)
            future_to_url = {executor.submit(_update, next(url_iterator), new_name): new_name for new_name in new_names}
            count = 0
            for future in futures.as_completed(future_to_url):
                count += 1
                # new_name = future_to_url[future]
                try:
                    future.result()
                except Exception:
                    raise
                else:
                    print("+", end="")
                    if count % 100 == 0:
                        print("")

        print("Finished. Now checking...")

        # Assert model was created and audit exists
        assert SimpleAuditEntry.objects.all().count() == len(new_names)
        names_in_payload = [audit_entry.get_row_data()["name"] for audit_entry in SimpleAuditEntry.objects.all()]
        assert len(names_in_payload) == len(new_names)
        assert set(names_in_payload) == set(new_names)
