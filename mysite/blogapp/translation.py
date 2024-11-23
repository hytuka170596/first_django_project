from modeltranslation.translator import TranslationOptions, register
from .models import Tag, Category, Author, Article


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    """Translation options for the Tag model."""

    fields = ("name_tag",)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Translation options for the Category model."""

    fields = ("name_category",)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    """Translation options for the Author model."""

    fields = ("name_author",)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    """Translation options for the Article model."""

    fields = (
        "title",
        "content",
    )
