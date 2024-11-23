from django.core.management import BaseCommand
from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        order = Order.objects.first()
        if not order:
            self.stdout.write("No order found")

        products = Product.objects.all()
        order.products.add(*products)

        order.save()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully added product {curr_product} to order {order}".format(
                    curr_product=order.products.all(), order=order
                )
            )
        )
