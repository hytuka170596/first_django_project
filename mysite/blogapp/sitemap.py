from django.contrib.sitemaps import Sitemap
from django.db.models import DateTimeField

from .models import Article


class BlogSitemap(Sitemap):
    """Sitemap for blog."""

    changefreq: str = "weekly"
    priority: float = 0.5

    def items(self) -> list[Article]:
        """Returns all articles that have passed the filter."""
        return Article.objects.filter(archived__isnull=False).order_by("pk")

    def lastmod(self, obj: Article) -> DateTimeField:
        """Returns the last modification date of the article."""
        return obj.pub_date
