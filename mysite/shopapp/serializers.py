"""
Module for serializing and deserializing models for REST API applications Shopapp.
"""

from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from .models import Product, Order
from django.db.models import Model
from typing import Tuple


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer handles the serialization and deserialization of
    Product instances, including read-only fields for the creator's
    username and ID.

    Attributes:
        creator_product (ReadOnlyField): The username of the user who created the product.
        creator_id (ReadOnlyField): The ID of the user who created the product.
        product_id (ReadOnlyField): The ID of the product.

    Meta:
        model (Product): The Product model associated with this serializer.
        fields (tuple): A tuple of field names to include in the serialized output.
    """

    creator_product: ReadOnlyField = serializers.ReadOnlyField(
        source="created_by.username"
    )
    creator_id: ReadOnlyField = serializers.ReadOnlyField(source="created_by.id")
    product_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model: Model = Product
        fields: Tuple[str] = (
            "creator_product",
            "creator_id",
            "product_id",
            "name",
            "price",
            "description",
            "discount",
            "created_at",
            "archived",
            "preview",
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer handles the serialization and deserialization of
    Order instances, including read-only fields for the customer's
    username and ID, as well as nested serialization for products.

    Attributes:
        customer (ReadOnlyField): The username of the customer placing the order.
        customer_id (ReadOnlyField): The ID of the customer placing the order.
        products (ProductSerializer): A nested serializer for related Product instances.

    Meta:
        model (Order): The Order model associated with this serializer.
        fields (tuple): A tuple of field names to include in the serialized output.
    """

    customer: ReadOnlyField = serializers.ReadOnlyField(source="user.username")
    customer_id: ReadOnlyField = serializers.ReadOnlyField(source="user.id")
    products: ProductSerializer = ProductSerializer(many=True)

    class Meta:
        model: Model = Order
        fields: Tuple[str] = (
            "customer",
            "customer_id",
            "products",
            "id",
            "delivery_address",
            "promocode",
            "phone",
            "created_at",
            "receipt",
        )
