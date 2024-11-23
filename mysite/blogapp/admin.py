from django.contrib import admin
from .models import Tag, Author, Article, Category

from typing import Tuple


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """The TagAdmin adds this model(Tag) to the admin panel"""

    list_display: Tuple[str] = (
        "id",
        "name_tag_en",
        "name_tag_ru",
    )
    search_fields: Tuple[str] = (
        "id",
        "name_tag_en",
        "name_tag_ru",
    )
    ordering: Tuple[str] = ("id",)
    list_display_links: Tuple[str] = (
        "id",
        "name_tag_en",
        "name_tag_ru",
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """The AuthorAdmin adds this model(Author) to the admin panel"""

    list_display: Tuple[str] = (
        "id",
        "name_author_en",
        "name_author_ru",
    )
    search_fields: Tuple[str] = (
        "id",
        "name_author_en",
        "name_author_ru",
    )
    ordering: Tuple[str] = ("id",)
    list_display_links: Tuple[str] = (
        "id",
        "name_author_en",
        "name_author_ru",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """The CategoryAdmin adds this model(Category) to the admin panel"""

    list_display: Tuple[str] = (
        "id",
        "name_category_en",
        "name_category_ru",
    )
    search_fields: Tuple[str] = (
        "id",
        "name_category_en",
        "name_category_ru",
    )
    ordering: Tuple[str] = ("id",)
    list_display_links: Tuple[str] = (
        "id",
        "name_category_en",
        "name_category_ru",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """The ArticleAdmin adds this model(Article) to the admin panel"""

    list_display: Tuple[str] = (
        "id",
        "pub_date",
        "author",
        "category",
        "title_en",
        "content_en",
        "title_ru",
        "content_ru",
    )
    search_fields: Tuple[str] = (
        "id",
        "pub_date",
        "author",
        "category",
        "title_en",
        "content_en",
        "title_ru",
        "content_ru",
    )
    ordering: Tuple[str] = (
        "id",
        "pub_date",
        "author",
        "category",
        "title_en",
        "content_en",
        "title_ru",
        "content_ru",
    )
    list_display_links: Tuple[str] = (
        "id",
        "pub_date",
        "author",
        "category",
        "title_en",
        "content_en",
        "title_ru",
        "content_ru",
    )
