from django.core.management import BaseCommand


from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.SUCCESS("Start demo bulk actions"))
        # Обращаясь через фильтр к модели с аргументом name__contains(равносильно оператору LIKE в SQL) мы ищем
        # соответствия и через метод update с аргументами kwargs мы обновляем все записи в бд.
        result_update = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)
        print(result_update)

        # Здесь всего одним запросом делается заполнение бд нашими данными.
        info = [("Smartphone 1", 199), ("Smartphone 2", 299), ("Smartphone 3", 399)]
        products = [Product(name=name, price=price) for name, price in info]

        result = Product.objects.bulk_create(products)

        for obj in result:
            print(obj)

        self.stdout.write("Done")
