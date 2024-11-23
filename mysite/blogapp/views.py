from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet, Model, CharField, TextField
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.syndication.views import Feed
from .forms import ArticleForm
from .models import Article, Tag

from typing import Tuple


class ArticlesListView(ListView):
    """View list all articles"""

    template_name: str = "blogapp/article_list.html"
    queryset: QuerySet[Model] = (
        Article.objects.filter(pub_date__isnull=False)
        .prefetch_related("tags")
        .select_related("author")
        .defer("content")
    )
    context_object_name: str = "articles"


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    """View detail article by id"""

    permission_required: Tuple[str] = ("blogapp.view_article",)
    template_name: str = "blogapp/article_detail.html"
    model: Model = Article
    context_object_name: str = "article"


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    """View update article by id"""

    permission_required: Tuple[str] = ("blogapp.change_article",)
    template_name: str = "blogapp/article_update.html"
    model: Model = Article
    context_object_name: str = "article"
    form_class: ModelForm = ArticleForm

    def get_success_url(self) -> HttpResponse:
        return reverse(
            viewname="blogapp:article_details", kwargs={"pk": self.object.pk}
        )


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    """View create new article"""

    permission_required: Tuple[str] = ("blogapp.add_article",)
    template_name: str = "blogapp/article_create.html"
    model: Model = Article
    context_object_name: str = "article"
    form_class: ModelForm = ArticleForm
    success_url: str = reverse_lazy("blogapp:articles_list")

    def get_success_url(self) -> HttpResponse:
        return reverse(viewname="blogapp:article_detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    """View delete article by id"""

    permission_required: Tuple[str] = ("blogapp.delete_article",)
    template_name: str = "blogapp/article_delete.html"
    model: Model = Article
    success_url: str = reverse_lazy("blogapp:articles_list")


class LatestArticlesFeed(Feed):
    """RSS feed for latest articles"""

    title: str = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles_list")

    def items(self) -> QuerySet[Article]:
        """Returns the first five articles for RSS feed"""
        return (
            Article.objects.filter(pub_date__isnull=False)
            .prefetch_related("tags")
            .select_related("author")
            .defer("content")[:5]
        )

    def item_title(self, item: Article) -> CharField:
        """Returns the title of the article in RSS feed"""
        return item.title

    def item_description(self, item: Article) -> TextField:
        """Returns the description of the article, but within 200 characters"""
        return item.content[:200]

    def item_link(self, item: Article) -> str:
        """Returns the link to the article in the RSS feed"""
        return reverse(viewname="blogapp:article_detail", kwargs={"pk": item.pk})
