import copy
from dataclasses import dataclass
from uuid import UUID
import factory
from factory.helpers import lazy_attribute
import factory.random
from faker import Faker
from datetime import datetime

factory.random.reseed_random("pypes")
Faker.seed("pypes")
fake = Faker()

NUM_CUSTOMERS = 20
NUM_ITEMS = 100
NUM_ORDERS = 1000


@dataclass
class Item:
    description: str
    barcode: str


@dataclass
class Customer:
    uid: UUID
    name: str
    address: str
    email_address: str
    country: str


@dataclass
class Order:
    uid: UUID
    items: list[Item]
    customer: Customer
    currency: str
    credit_card: str
    order_timestamp: datetime


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    description = factory.Faker("paragraph")
    barcode = factory.Faker("ean", length=13)


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    uid = factory.Faker("uuid4")
    name = factory.Faker("company")
    address = factory.Faker("address")
    country = factory.Faker("country")
    email_address = factory.Faker("company_email")


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    class Params:
        customers = None
        available_items = None

    uid = factory.Faker("uuid4")
    customer = factory.LazyAttribute(
        lambda o: fake.random_element(elements=o.customers)
    )
    currency = factory.Faker("currency")
    credit_card = factory.Faker("credit_card_provider")
    order_timestamp = factory.Faker(
        "date_time_between", start_date="-1y", end_date="now"
    )

    @lazy_attribute
    def items(self) -> list[Item]:
        items = fake.random_choices(self.available_items)
        items = copy.deepcopy(items)
        for item in items:
            faulty = fake.boolean(chance_of_getting_true=3)
            if faulty:
                item.barcode += fake.pystr()
                # Oops faulty barcode!
        return items


def main():
    print("Generating customers")

    customers = [CustomerFactory() for i in range(NUM_CUSTOMERS)]
    print("Generating items")
    items = [ItemFactory() for i in range(NUM_ITEMS)]
    orders = [
        OrderFactory(customers=customers, available_items=items)
        for i in range(NUM_ORDERS)
    ]

    filtered_orders = []
    for order in orders:
        if (
            len(order.items) > 20
            and "Visa" in order.credit_card
            and any(len(item.barcode) != 13 for item in order.items)
        ):
            filtered_orders.append(order)

    print(len(filtered_orders))


if __name__ == "__main__":
    main()
