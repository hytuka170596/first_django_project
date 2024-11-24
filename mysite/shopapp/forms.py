"""
Module for handling forms and validation Products and Orders.
"""

import json

from django import forms
from django.contrib.auth.models import Group
from django.forms import Field
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Product, Order
from django.db.models import Model
import os
import re
from typing import List, Dict, Tuple, Optional, Union
from django.db.models import DecimalField
from PIL import ImageFile


def get_list_promocode() -> List:
    __SECOND_PROMOCODE_LIST: List[str] = ["SALE1", "SALE2", "SALE3", "SALE4", "SALE5"]
    __script_dir: str = os.path.dirname(__file__)
    __file_path: str = os.path.abspath(
        os.path.join(__script_dir, "promocodes_list.txt")
    )
    try:
        with open(file=__file_path, mode="r", encoding="utf-8") as file:
            __PROMOCODE_LIST: List[str] = file.read().splitlines()
            return __PROMOCODE_LIST
    except FileNotFoundError:
        __PROMOCODE_LIST: List[str] = __SECOND_PROMOCODE_LIST


def check_phone_number(phone_number: str) -> None:
    """
    Validate the provided phone number against predefined patterns.

    Args:
        phone_number (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number does not match the expected formats.
    """
    pattern_1: str = r"^\+?\d{1,3} ?(\(\d{1,3}\)|\d{1,3}) ?\d{3}[- ]?\d{2}[- ]?\d{2}$"
    pattern_2: str = r"^\+?\d{10,15}$"

    if re.match(pattern_1, phone_number) or re.match(pattern_2, phone_number):
        return
    else:
        raise ValidationError(
            _("Enter the phone number in the format +7 (123) 456-7890 or +1234567890")
        )


def check_promocode(promocode: Optional[str]) -> None:
    """
    Validate the provided promocode.

    Args:
        promocode (Optional[str]): The promocode to validate. Can be None or an empty string.

    Raises:
        ValidationError: If the promocode is invalid or expired.
    """
    if promocode is None or promocode == "":
        return  # Allow empty strings or None
    elif promocode in get_list_promocode():
        return
    else:
        raise ValidationError(
            _("There is no such promo code or its expiration date has expired")
        )


class MultipleImageInput(forms.ClearableFileInput):
    """
    Custom file input widget that allows multiple file selections.

    Attributes:
        allow_multiple_selected (bool): Indicates that multiple files can be selected.
    """

    allow_multiple_selected: bool = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, images: Union[List[ImageFile], ImageFile], initial=None, **kwargs):
        super().__init__(*args, initial=initial, **kwargs)
        self.images = images

# class MultipleImageField(forms.FileField):
#     """
#     Custom form field for handling multiple image uploads.

#     Args:
#         *args: Positional arguments for the parent class.
#         **kwargs: Keyword arguments for the parent class.

#     Methods:
#         clean(images: Union[List[files], files], initial=None) -> Union[List[files], files]:
#             Cleans and validates uploaded images.
#     """

#     def __init__(self, *args, **kwargs) -> None:
#         kwargs.setdefault("widget", MultipleImageInput())
#         super().__init__(*args, **kwargs)

#     def clean(
#         self, images: Union[List[ImageFile], ImageFile], initial=None
#     ) -> Union[List[ImageFile], ImageFile]:
#         """
#         Clean and validate uploaded images.

#         Args:
#             images (Union[List[ImageFile], ImageFile]): The uploaded images to clean.
#             initial: Initial data for cleaning.

#         Returns:
#             Union[List[ImageFile], ImageFile]: A list of cleaned images or a single cleaned image.
#         """

#         single_file_clean = super().clean
#         if isinstance(images, (list, tuple)):
#             result: List[ImageFile] = [
#                 single_file_clean(image, initial) for image in images
#             ]
#         else:
#             result: ImageFile = [single_file_clean(images, initial)]

#         return result


class ProductForm(forms.ModelForm):
    """
    Form for creating or updating products.

    Attributes:
        image (MultipleImageField): Field for uploading multiple product images.

    Meta:
        model (Model): The Product model associated with this form.
        fields (List[str]): List of fields to include in the form.
        labels (Dict[str, str]): Labels for each field in the form.

    Methods:
        clean_price() -> float | DecimalField:
            Validates the price field to ensure it is greater than zero.
    """

    image: MultipleImageField = MultipleImageField(
        required=False,
        label=_("Images"),
        help_text=_("A field for adding multiple product photos"),
    )

    class Meta:
        model: Model = Product
        fields: List[str] = [
            "name",
            "price",
            "description",
            "discount",
            "preview",
        ]
        labels: Dict[str, str] = {
            "name": _("Name"),
            "price": _("Price"),
            "description": _("Description"),
            "discount": _("Discount"),
            "preview": _("Preview"),
        }

    def clean_price(self) -> float | DecimalField:
        """
        Validate the price field to ensure it is greater than zero.

        Returns:
            float | DecimalField: The validated price.

        Raises:
            forms.ValidationError: If the price is less than or equal to zero.
        """

        data: float | DecimalField = self.cleaned_data["price"]

        if data <= 0:
            raise forms.ValidationError(_("Price must be greater than zero."))

        return data


class OrderForm(forms.ModelForm):
    """
     Form for creating or updating orders.

     Meta:
        model (Model): The Order model associated with this form.
        fields (List[str]): List of fields to include in the form.
        widgets (Dict[str, forms.Textarea]): Custom widgets for specific fields.
        labels (Dict[str, str]): Labels for each field in the form.

    Methods:
        clean_promocode() -> str:
            Validates the promocode field using `check_promocode`.
        clean_phone() -> str:
            Validates the phone number field using `check_phone_number`.
    """

    class Meta:
        model: Model = Order
        fields: List[str] = [
            "delivery_address",
            "promocode",
            "products",
            "user",
            "phone",
        ]
        widgets: Dict[str, forms.Textarea] = {
            "delivery_address": forms.Textarea(attrs={"cols": 30, "rows": 2}),
        }
        labels: Dict[str, str] = {
            "delivery_address": _("Delivery address"),
            "promocode": _("Promocode"),
            "products": _("Products"),
            "user": _("User"),
            "phone": _("Phone"),
        }

    def clean_promocode(self) -> str:
        """
        Validate the promocode field using `check_promocode`.

        Returns:
            str: The validated promocode.

        Raises:
            ValidationError: If the promocode is invalid.
        """

        promocode: str = self.cleaned_data.get("promocode")
        check_promocode(promocode)
        return promocode

    def clean_phone(self) -> str:
        """
        Validate the phone number field using `check_phone_number`.

        Returns:
            str: The validated phone number.

        Raises:
            ValidationError: If the phone number is invalid.
        """

        phone: str = self.cleaned_data.get("phone")
        check_phone_number(phone)
        return phone


class GroupForm(forms.ModelForm):
    """
     Form for creating or updating user groups.

    Meta:
       model (Model): The Group model associated with this form.
       fields (Tuple[str]): List of fields to include in the form.
       labels (Dict[str, str]): Labels for each field in the form.
    """

    class Meta:
        model: Model = Group
        fields: Tuple[str] = ("name",)
        labels: Dict[str, str] = {
            "name": _("Name"),
        }


class CSVImportForm(forms.Form):
    """Form for importing CSV data."""

    csv_file: Field = forms.FileField(label=_("CSV file"))

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get("csv_file")
        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError(_("The file must have an extension .csv"))
        return csv_file


class JSONImportForm(forms.Form):
    """Form for importing JSON data."""

    json_file: Field = forms.FileField(
        label=_("JSON file"),
    )

    def clean_json_file(self):
        """Validates the JSON file."""
        json_file = self.cleaned_data.get("json_file")
        if not json_file.name.endswith(".json"):
            raise forms.ValidationError(_("The file must have an extension .json"))
        try:
            data = json.load(json_file)
            validated_orders = []
            for order_data in data:
                form: OrderForm = OrderForm(data=order_data)
                if not form.is_valid():
                    error_messages = form.errors.as_data()
                    raise forms.ValidationError(error_messages)
                validated_orders.append(form.cleaned_data)
            return json_file

        except json.JSONDecodeError:
            raise forms.ValidationError(_("Invalid JSON format"))
        except Exception as error_message:
            raise forms.ValidationError(str(error_message))
