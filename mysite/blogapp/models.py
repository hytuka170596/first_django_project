from django.db import models
from django.db.models import TextField, CharField, DateTimeField, BooleanField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from typing import List, Tuple


class Author(models.Model):
    """The Author model represents the author of the article"""

    class Meta:
        ordering: List[str] = ["pk"]
        verbose_name: Tuple[str] = _("Author")
        verbose_name_plural: Tuple[str] = _("Authors")

    name_author: CharField = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
        default="Name of the author",
        unique=True,
    )
    bio: TextField = models.TextField(
        null=False, blank=True, db_index=True, default="Bio of the author"
    )
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    last_updated: DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> CharField:
        return self.name_author


class Category(models.Model):
    """The Category model represents the category of an article."""

    class Meta:
        ordering: List[str] = ["pk"]
        verbose_name: Tuple[str] = _("Category")
        verbose_name_plural: Tuple[str] = _("Categories")

    name_category: CharField = models.CharField(
        max_length=40, null=False, blank=False, db_index=True
    )

    def __str__(self) -> CharField:
        return self.name_category


class Tag(models.Model):
    """The Tag model represents a tag that can be assigned to an article"""

    class Meta:
        ordering: List[str] = ["pk"]
        verbose_name: Tuple[str] = _("Tag")
        verbose_name_plural: Tuple[str] = _("Tags")

    name_tag: CharField = models.CharField(
        max_length=20, null=False, blank=False, db_index=True
    )

    def __str__(self) -> CharField:
        return self.name_tag


class Article(models.Model):
    """The Article model represents an article."""

    class Meta:
        ordering: List[str] = ["-pub_date"]
        verbose_name: Tuple[str] = _("Article")
        verbose_name_plural: Tuple[str] = _("Articles")

    title: CharField = models.CharField(
        max_length=100, null=False, blank=False, db_index=True
    )
    content: TextField = models.TextField(
        null=False,
        blank=False,
    )
    pub_date: DateTimeField = models.DateTimeField(null=True, blank=True)
    author: Author = models.ForeignKey(
        to=Author, on_delete=models.CASCADE, db_index=True
    )
    category: Category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    tags: List[Tag] = models.ManyToManyField(to=Tag, blank=True)
    archived: BooleanField = models.BooleanField(
        default=False,
        help_text=_("Check the box if you want to hide this article"),
    )

    def __str__(self) -> CharField:
        return self.title

    def __repr__(self) -> str:
        return f"<Article: {self.pk}>"

    def get_absolute_url(self) -> str:
        """Returns the absolute url of the article"""
        return reverse("blogapp:article_detail", kwargs={"pk": self.pk})
