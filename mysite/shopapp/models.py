"""
Module containing the model application Shopapp.
"""

from django.urls import reverse

from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

from django.db.models import (
    CharField,
    TextField,
    DecimalField,
    ImageField,
    PositiveSmallIntegerField,
    DateTimeField,
    BooleanField,
    ForeignKey,
    Model,
    ManyToManyField,
    FileField,
)
from django.utils.translation import gettext_lazy as _

from typing import List, Tuple


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    """
    Generate the directory path for storing product preview images.

    This function constructs a file path for storing the preview image
    associated with a specific product. The path includes the product's
    primary key to ensure that preview images are organized by product.

    Args:
        instance (Product): The instance of the Product model associated
                            with the preview image.
        filename (str): The name of the preview image file being uploaded.

    Returns:
        str: The formatted directory path where the preview image will be
             stored, e.g., "products/product_{ID}/preview/{filename}".
    """
    return "products/product_{ID}/preview/{filename}".format(
        ID=instance.pk, filename=filename
    )


class Product(models.Model):
    """
    Represents a product in the inventory.

    Attributes:
        name (str): The name of the product, with a maximum length of 100 characters.
        description (str): A text description of the product. Can be left blank but cannot be null.
        price (Decimal): The price of the product, with a maximum of 8 digits, including 2 decimal places. Defaults to 0.
        discount (int): The discount percentage applied to the product, represented as a small integer. Defaults to 0.
        created_at (datetime): The date and time when the product was created. Automatically set when the product is created.
        archived (bool): Indicates whether the product is archived. Defaults to False.
    """

    class Meta:
        ordering: List[str] = ["name", "price"]
        verbose_name: Tuple[str] = _("Product")
        verbose_name_plural: Tuple[str] = _("Products")

    name: CharField = models.CharField(
        max_length=100, null=False, blank=False, db_index=True
    )
    description: TextField = models.TextField(null=False, blank=True, db_index=True)
    price: DecimalField = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount: PositiveSmallIntegerField = models.PositiveSmallIntegerField(default=0)
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    archived: BooleanField = models.BooleanField(default=False)
    created_by: ForeignKey = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, blank=True
    )
    preview: ImageField = models.ImageField(
        null=True, blank=True, upload_to=product_preview_directory_path
    )

    @property
    def description_short(self) -> TextField:
        """Return a short description of the product."""
        if len(self.description) < 80:
            return self.description
        return self.description[:80] + "..."

    @property
    def final_price(self) -> Decimal:
        """Return the final price of the product after applying the discount."""
        return self.price - self.price * self.discount / 100

    def __str__(self) -> CharField:
        """Return the name of the product as a string."""
        return self.name

    def get_absolute_url(self) -> str:
        """Return the URL of the product by its primary key"""
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})


def product_images_directory_path(instance: "ProductImage", image_name: str) -> str:
    """
    Generate the directory path for storing product images.

    This function constructs a file path for storing images associated
    with a specific product. The path includes the product's primary key
    to ensure that images are organized by product.

    Args:
        instance (ProductImage): The instance of the ProductImage model
                                 associated with the image.
        image_name (str): The name of the image file being uploaded.

    Returns:
        str: The formatted directory path where the image will be stored,
             e.g., "products/product_{ID}/images/{image_name}".
    """
    return "products/product_{ID}/images/{image_name}".format(
        ID=instance.product.pk, image_name=image_name
    )


class ProductImage(models.Model):
    """
    Model representing an image associated with a product.

    This model stores images for products in the application. Each image
    can have an optional description and is linked to a specific product.

    Attributes:
        product (ForeignKey): A foreign key linking to the Product model.
                              This establishes a one-to-many relationship
                              where one product can have multiple images.
        image (ImageField): The image file associated with the product.
                            The file will be stored in a directory defined
                            by the `product_images_directory_path` function.
        description (CharField): An optional description for the image with
                                 a maximum length of 200 characters.
    """

    product: Model = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="images"
    )
    image: ImageField = models.ImageField(upload_to=product_images_directory_path)
    description: CharField = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    """
    Represents an order placed by a user.

    Attributes:
        delivery_address (str): The delivery address for the order. Can be left blank or null.
        promocode (str): A promotional code applied to the order. Can be left blank but cannot be null. Maximum length is 20 characters.
        created_at (datetime): The date and time when the order was created. Automatically set when the order is created.
        user (User): A reference to the user who placed the order. If the user is deleted, the order remains (using PROTECT).
        products (ManyToManyField): A many-to-many relationship with the `Product` model. Allows an order to include multiple products.
                                    The related name 'orders' allows accessing all orders for a product.
    """

    class Meta:
        ordering: List[str] = ["-pk"]
        verbose_name: Tuple[str] = _("Order")
        verbose_name_plural: Tuple[str] = _("Orders")

    delivery_address = models.TextField(
        null=False, blank=True, default=" # Russia, Moscow, Ul. Mira. d. 144/2  "
    )
    promocode = models.CharField(
        max_length=20, default=" # 123sale123", null=False, blank=True
    )
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    user: User = models.ForeignKey(User, on_delete=models.PROTECT)
    products: ManyToManyField = models.ManyToManyField(
        to=Product, related_name="orders"
    )
    phone: CharField = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="+7(999) 999-9999",
    )
    receipt: FileField = models.FileField(null=True, upload_to="orders/receipts/")

    def __str__(self) -> str:
        """Return a string representation of the order."""
        return "Order #{order_id}".format(order_id=self.id)
