from typing import Tuple

from modeltranslation.translator import TranslationOptions, register
from .models import Product, Order


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields: Tuple[str] = ("name", "description")
