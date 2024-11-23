"""
Module containing the urls of the application Shopapp.
"""

from django.urls import path, include
from .views import (
    ShopIndexView,
    GroupListView,
    ProductDetailsView,
    ProductsListView,
    OrderListView,
    OrderDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDataExportView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrderDataExportView,
    UserDetailsView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrderDataExportView,
)

from typing import List
from rest_framework.routers import DefaultRouter


app_name: str = "shopapp"
router: DefaultRouter = DefaultRouter()
router.register(prefix="products", viewset=ProductViewSet, basename="product")
router.register(prefix="orders", viewset=OrderViewSet, basename="order")

urlpatterns: List[path] = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(router.urls)),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/archive/",
        ProductDeleteView.as_view(),
        name="product_archive",
    ),
    path("products/latest/feed/", LatestProductsFeed(), name="latest_products_feed"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/export/", OrderDataExportView.as_view(), name="orders-export"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path(
        "orders/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order_delete",
    ),
    path("user/<int:pk>/", UserDetailsView.as_view(), name="user_details"),
    path(
        "users/<int:pk>/orders/", UserOrdersListView.as_view(), name="user_orders_list"
    ),
    path(
        "users/<int:pk>/orders/export/",
        UserOrderDataExportView.as_view(),
        name="user_orders_list_export",
    ),
]
