"""Regroup a set of functions and helpers to manage simulation environments."""

from faker import Faker
from faker.providers import internet


def simulate_ip_address():
    """Get a mock ip address.

    Returns:
        str: an ip address v4
    """
    fake = Faker(["es_ES"])
    fake.add_provider(internet)
    return fake.ipv4()
