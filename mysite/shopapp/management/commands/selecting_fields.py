from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import QuerySet

from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.SUCCESS("Start demo select fields"))
        users_info: QuerySet = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)

        products_values = Product.objects.values("pk", "name_ru")
        for product_value in products_values:
            print(product_value)
        self.stdout.write("Done")
