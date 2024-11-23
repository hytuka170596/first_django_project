from django.urls import path

from .views import (
    hello_world_view,
    GroupsListView,
    UsersListView,
    ArticleListView,
    ArticleCreateView,
    ProfilesListView,
)


app_name = "myapiapp"
urlpatterns = [
    path("hello/", hello_world_view, name="hello_world"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    path("users/", UsersListView.as_view(), name="users"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("profiles/", ProfilesListView.as_view(), name="profiles"),
]
