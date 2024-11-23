"""
Module containing the urls of the application.
"""

from django.contrib.auth.views import LoginView
from django.urls import path
from typing import List
from .views import (
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    ProfileUpdateView,
    ProfileListView,
    ProfileDetailsView,
    HelloView,
)


app_name: str = "myauth"

urlpatterns: List[path] = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path(
        "details/profile_id/<int:pk>",
        ProfileDetailsView.as_view(),
        name="profile-details",
    ),
    path(
        "update/profile_id/<int:pk>", ProfileUpdateView.as_view(), name="profile-update"
    ),
    path("profiles/", ProfileListView.as_view(), name="profiles-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
