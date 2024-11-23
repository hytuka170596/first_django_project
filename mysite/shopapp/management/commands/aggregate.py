from django.core.management import BaseCommand
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.SUCCESS("Start demo aggregate"))

        result = Product.objects.aggregate(
            Avg("price"),
            Max("price"),
            Min("price"),
            Count("id"),
        )
        print(result)

        result_with_filter = Product.objects.filter(
            name__contains="Smartphone"
        ).aggregate(
            Avg("price"),
            Max("price"),
            my_min_price=Min("price"),
            my_count=Count("id"),
        )
        # Можно делать методы агрегации именованными, чтобы при выводе видеть именно так как вам необходимо.
        # Но так как это именованные аргументы, их нужно указывать только после позиционных!
        print(result_with_filter)

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count(
                "products",
            ),
        )
        for order in orders:
            print(
                f"Order #{order.id} "
                f"with {order.products_count} "
                f"products worth {order.total} "
            )
        self.stdout.write("Done")
