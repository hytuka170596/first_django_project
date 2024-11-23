from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    A custom management command to create an order for a specified user.

    This command retrieves the user based on the provided username and creates an order
    with a specified delivery address and promotional code. If the order already exists
    with the same details, it will not be created again.

    Methods:
        handle(*args, **options) -> None:
            Executes the command, creating the order with given or default details.
            Outputs success messages to the console, including details of the created order.

    """

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.SUCCESS("Create order with products"))
        user = User.objects.get(username="admin")
        # Метод defer исключает из запроса те поля, которые указаны в методе,
        # его используют, если этими полями точно никто не будет пользоваться,
        # иначе они будут добавлены в запрос, что излишне нагружает сервер.
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at",).all()
        products: Sequence[Product] = Product.objects.only("id").all()
        # Это противоположный метод, он выберет только те поля, которые указаны в методе.
        order, _ = Order.objects.get_or_create(
            delivery_address="ul Mira, d 100",
            promocode="SALE111",
            user=user,
        )
        for product in products:
            order.products.add(product)
        self.stdout.write(
            self.style.SUCCESS(
                "Order created {current_order}".format(current_order=order)
            )
        )
