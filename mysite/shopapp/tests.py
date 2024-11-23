"""
Module for unit testing of views and the shopapp application
"""

from http.client import HTTPResponse

from django.contrib.auth.models import Permission, User
from django.db.models import QuerySet
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from shopapp.utils import add_two_numbers
from shopapp.models import Product, Order
from string import ascii_letters
from random import choices
from typing import List, Dict


class AddTwoNumbersTestCase(TestCase):
    """
    Test case for the add_two_numbers function
    """

    def test_two_numbers(self) -> None:
        result: int = add_two_numbers(4, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    """
    Test case for the ProductCreateView
    """

    def setUp(self) -> None:
        self.user: User = User.objects.create_superuser(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.product_name: str = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self) -> None:
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.4",
                "description": "A good table",
                "discount": "10",
            },
        )
        self.assertRedirects(
            response=response, expected_url=reverse("shopapp:products_list")
        )


class ShopAppTestCase(TestCase):
    """
    Test case for the shopapp application
    """

    @classmethod
    def create_user_with_permission(
        cls, username: str, email: str, password: str, permission_codename: str
    ) -> User:
        user: User = User.objects.create_user(
            username=username, email=email, password=password
        )
        permission: Permission = Permission.objects.get(
            codename=permission_codename, content_type__app_label="shopapp"
        )
        user.user_permissions.add(permission)
        return user

    @classmethod
    def create_product(
        cls, name: str, price: str, description: str, discount: str
    ) -> Product:
        product: Product = Product.objects.create(
            name=name, price=price, description=description, discount=discount
        )
        return product


class ProductDetailsViewTestCase(ShopAppTestCase):
    """
    Test case for the ProductDetailsView
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.product_name: str = "".join(choices(ascii_letters, k=10))
        cls.product: Product = Product.objects.create(name=cls.product_name)
        cls.user: User = cls.create_user_with_permission(
            "testuser", "test@example.com", "password", "change_product"
        )

    def setUp(self) -> None:
        super().setUp()
        self.client.login(username="testuser", password="password")

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.user.delete()
        cls.product.delete()

    def test_get_product(self) -> None:
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self) -> None:
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(ShopAppTestCase):
    fixtures: list[str] = ["products-fixture.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = cls.create_user_with_permission(
            "testuser", "test@example.com", "password", "view_product"
        )

    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.user.delete()

    def test_products(self) -> None:
        response = self.client.get(path=reverse(viewname="shopapp:products_list"))
        # products = Product.objects.filter(archived=False).all()
        # products_context = response.context.get("products")
        # for product_1, product_2 in zip(products, products_context):
        #     self.assertEqual(product_1.pk, product_2.pk)
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(product.pk for product in response.context.get("products")),
            transform=lambda product: product.pk,
        )
        self.assertTemplateUsed(
            response=response, template_name="shopapp/products-list.html"
        )


class ProductsExportViewTestCase(TestCase):
    """
    Test case for the ProductsExportView
    """

    fixtures: list[str] = ["products-fixture.json"]

    def test_get_products_view(self) -> None:
        response: HTTPResponse = self.client.get(
            path=reverse("shopapp:products-export"),
        )
        self.assertEqual(first=response.status_code, second=200)
        products: QuerySet[Product] = Product.objects.order_by("pk").all()
        expected_data: List[dict[str, str]] = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data: Dict[str, str] = response.json()
        self.assertEqual(first=products_data.get("products"), second=expected_data)


class OrdersListViewTestCase(TestCase):
    """
    Test case for the OrdersListView
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = User.objects.create_user(
            username="testuser", password="password"
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_orders_view(self) -> None:
        response = self.client.get(path=reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self) -> None:
        self.client.logout()
        response = self.client.get(path=reverse("shopapp:orders_list"))
        self.assertEqual(
            first=response.status_code,
            second=302,
        )
        self.assertIn(member=str(settings.LOGIN_URL), container=response.url)


class OrderDetailViewTestCase(ShopAppTestCase):
    """
    Test case for the OrderDetailView
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = cls.create_user_with_permission(
            username="testuser",
            email="test@example.com",
            password="password",
            permission_codename="view_order",
        )
        cls.product: Product = cls.create_product(
            name="test product",
            price="123.4",
            description="A good product",
            discount="10",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.user.delete()
        cls.product.delete()

    def setUp(self) -> None:
        super().setUp()

        self.client.force_login(self.user)
        self.order: Order = Order.objects.create(
            user=self.user,
            promocode="SALE1",
            delivery_address="123 Main St",
            phone="+7(999) 999-9999",
        )
        self.order.products.add(self.product)

    def tearDown(self) -> None:
        super().tearDown()
        self.order.delete()

    def test_order_details(self) -> None:
        response = self.client.get(
            path=reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(first=response.status_code, second=200)
        self.assertIn(
            member=self.order.delivery_address, container=str(response.content)
        )
        self.assertIn(member=self.order.promocode, container=str(response.content))
        self.assertEqual(first=response.context.get("order").pk, second=self.order.pk)
        self.assertEqual(first=response.context.get("order"), second=self.order)


class OrdersExportTestCase(ShopAppTestCase):
    """
    Test case for the OrdersExport
    """

    fixtures: list[str] = [
        "products-fixture.json",
        "orders-fixture.json",
        "users-fixture.json",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = User.objects.create_user(
            username="testuser",
            password="password",
            is_staff=True,
        )
        cls.product: Product = cls.create_product(
            name="test product",
            price="123.4",
            description="A good product",
            discount="10",
        )
        cls.order: Order = Order.objects.create(
            user=cls.user,
            promocode="SALE1",
            delivery_address="123 Main St",
            phone="+7(999) 999-9999",
        )
        cls.order.products.add(cls.product)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.user.delete()
        cls.product.delete()
        cls.order.delete()

    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_get_orders_view(self) -> None:
        response = self.client.get(path=reverse(viewname="shopapp:orders-export"))

        self.assertEqual(first=response.status_code, second=200)

        response_content: str = response.content.decode("utf-8")

        self.assertIn(str(self.order.user.pk), response_content)
        self.assertIn(self.order.delivery_address, response_content)
        self.assertIn(self.order.promocode, response_content)
        self.assertIn(str(self.order.pk), response_content)

        for product in self.order.products.filter(archived=False):
            self.assertIn(str(product.pk), response_content)
