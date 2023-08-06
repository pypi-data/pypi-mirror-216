import itertools
import os
import uuid
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

import pytest
import requests
from app.models import Customer
from django.urls import reverse

from django_partitioned_audit.models import SimpleAuditEntry
from tests.conftest import skipifadvanced

# pylint: skip-file


@skipifadvanced
@pytest.mark.skipif(os.environ.get("SKIP_SLOW"), reason="skipping slow tests")
@pytest.mark.django_db(transaction=True)
def test_concurrent_modifications(live_server, partition_created):
    customer = Customer.objects.create(name=str(uuid.uuid4()))
    urls = [
        f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=0",
        f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=100&post-wait-ms=0",
        f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=0&post-wait-ms=100",
        f"{live_server}{reverse('customer/update', args=[customer.pk])}?pre-wait-ms=100&post-wait-ms=100",
    ]

    def _update_customer(url: str, new_name: str):
        response = requests.post(url, data=dict(name=new_name))
        response.raise_for_status()

    new_names = [str(uuid.uuid4()) for _ in range(50)]

    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Start the load operations and mark each future with its URL
        url_iterator = itertools.cycle(urls)
        future_to_url = {
            executor.submit(_update_customer, next(url_iterator), new_name): new_name for new_name in new_names
        }
        for future in futures.as_completed(future_to_url):
            # new_name = future_to_url[future]
            try:
                future.result()
            except Exception:
                raise
            else:
                print("+", end="")

    # We need one audit entry for creation, then 1 audit entry for each update
    assert SimpleAuditEntry.objects.all().count() == len(new_names) + 1
    audit_entries: List[SimpleAuditEntry] = SimpleAuditEntry.objects.all()
    names_in_audit = [_.get_row_data()["name"] for _ in audit_entries]
    assert set(names_in_audit) == set([customer.name] + new_names)
