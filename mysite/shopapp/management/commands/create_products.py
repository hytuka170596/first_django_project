from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    A custom management command to create a predefined list of products.

    This command checks if each product in the predefined list exists in the database.
    If a product does not exist, it creates it. If it already exists, it skips creation.

    Methods:
        handle(*args, **options) -> None:
            Executes the command, creating the products if they do not already exist.
            Outputs success messages to the console.
    """

    def handle(self, *args, **options) -> None:
        self.stdout.write(msg=self.style.SUCCESS("Create products"))
        products_names = [
            "Laptop",
            "Desktop",
            "Smartphone",
        ]

        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(
                msg="Created product {curr_product}".format(curr_product=product.name)
            )

        self.stdout.write(self.style.SUCCESS("Products created"))
