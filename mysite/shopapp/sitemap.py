from django.contrib.sitemaps import Sitemap
from django.db.models import DateTimeField

from .models import Product


class ShopSitemap(Sitemap):
    changefreq: str = "hourly"
    priority: float = 0.5

    def items(self) -> list[Product]:
        """Returns a list of all products that have not been archived"""
        return Product.objects.filter(archived=False)

    def lastmod(self, obj: Product) -> DateTimeField:
        """Returns the time the product created"""
        return obj.created_at
