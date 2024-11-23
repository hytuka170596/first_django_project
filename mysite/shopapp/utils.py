from io import TextIOWrapper
from csv import DictReader
from typing import List, Optional, IO
from .models import Product, Order
import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


def add_two_numbers(a, b):
    return a + b


def save_csv_products(csv_file: IO[bytes], encoding: Optional[str]) -> List[Product]:
    csv_file = TextIOWrapper(csv_file, encoding=encoding)
    reader = DictReader(csv_file)

    products: List[Product] = [Product(**row) for row in reader]
    Product.objects.bulk_create(products)
    return products


def save_json_orders(json_file: IO[bytes], encoding: Optional[str]) -> List[Order]:
    """Save orders from JSON file to database"""
    json_file = TextIOWrapper(json_file, encoding=encoding)
    data_from_json_file = json.load(json_file)
    orders = []
    for order_data in data_from_json_file:
        if not isinstance(order_data, dict):
            raise TypeError("Each order must be a dictionary")

        product_id: List[int] = order_data.pop("products", [])
        user_id: Optional[List[int]] = order_data.pop("user", None)

        if user_id is not None:
            user: Optional[User] = get_object_or_404(User, id=user_id)
            order_data["user"] = user

        order: Order = Order(**order_data)
        order.save()
        order.products.set(Product.objects.filter(id__in=product_id))
        orders.append(order)

    return orders
