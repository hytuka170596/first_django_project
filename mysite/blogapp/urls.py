from django.urls import path

from .views import (
    ArticlesListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleCreateView,
    ArticleDeleteView,
    LatestArticlesFeed,
)

from typing import List

app_name: str = "blogapp"
urlpatterns: List[path] = [
    path("articles/", ArticlesListView.as_view(), name="articles_list"),
    path("articles/latest/feed", LatestArticlesFeed(), name="articles_feed"),
    path(
        "article/<int:pk>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "article/<int:pk>/update/", ArticleUpdateView.as_view(), name="article_update"
    ),
    path("article/create/", ArticleCreateView.as_view(), name="article_create"),
    path(
        "article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"
    ),
]
