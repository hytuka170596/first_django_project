from blogapp.sitemap import BlogSitemap
from django.contrib.sitemaps import Sitemap
from typing import Dict, Type


sitemaps: Dict[str, Type[Sitemap]] = {
    "blog": BlogSitemap,
}
