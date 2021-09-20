from dataclasses import dataclass
from uuid import UUID
import factory
import factory.random
from faker import Faker

factory.random.reseed_random("pypes")
Faker.seed("pypes")
fake = Faker()

NUM_CUSTOMERS = 20
NUM_ITEMS = 100
NUM_ORDERS = 1000


@dataclass
class Item:
    uid: UUID
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


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    uid = factory.Faker("uuid4")
    description = factory.Faker("paragraph")

    @factory.lazy_attribute
    def barcode(self):
        barcode = fake.ean(length=13)
        faulty = fake.boolean(chance_of_getting_true=10)

        if faulty:
            # Oops faulty barcode!
            barcode += fake.pystr()

        return barcode


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
        customers: list[Customer] = []
        available_items: list[Item] = []

    uid = factory.Faker("uuid4")
    customer = factory.LazyAttribute(
        lambda o: fake.random_element(elements=o.customers)
    )
    items = factory.LazyAttribute(lambda o: fake.random_choices(o.available_items))
    currency = factory.Faker("currency")
    credit_card = factory.Faker("credit_card_provider")


def main():
    print("Generating customers")

    customers = [CustomerFactory() for i in range(NUM_CUSTOMERS)]
    print("Generating items")
    items = [ItemFactory() for i in range(NUM_ITEMS)]
    OrderFactory(customers=customers, items=items)
    orders = [OrderFactory(items=items, customers=customers) for i in range(NUM_ORDERS)]
    print(customers[0])
    print(items[0])


if __name__ == "__main__":
    main()
