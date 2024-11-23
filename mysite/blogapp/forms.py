from typing import Tuple, Dict

from django.forms import Textarea
from django.forms import ModelForm
from .models import Author, Tag, Category, Article
from django.utils.translation import gettext_lazy as _
from django.db.models import Model
from django.db.models.fields import Field


class AuthorForm(ModelForm):
    """The form for creating an author"""

    class Meta:
        model: Model = Author
        fields: Tuple[Field] = ("name_author", "bio")
        labels: Dict[Field, str] = {"name_author": _("Name"), "bio": _("Bio")}


class TagForm(ModelForm):
    """The form for creating a tag"""

    class Meta:
        model: Model = Tag
        fields: Tuple[Field] = ("name_tag",)
        labels: Dict[Field, str] = {"name_tag": _("Name")}


class CategoryForm(ModelForm):
    """The form for creating a category"""

    class Meta:
        model: Model = Category
        fields: Tuple[Field] = ("name_category",)
        labels: Dict[Field, str] = {"name_category": _("Name")}


class ArticleForm(ModelForm):
    """The form for creating an article"""

    class Meta:
        model: Model = Article
        fields: Tuple[Field] = (
            "title",
            "content",
            "author",
            "tags",
            "category",
            "archived",
        )
        labels: Dict[Field, str] = {
            "title": _("Title"),
            "content": _("Content"),
            "author": _("Author"),
            "tags": _("Tags"),
            "category": _("Category"),
            "archived": _("Archived"),
        }
        widgets = {"content": Textarea(attrs={"cols": 50, "rows": 10})}
