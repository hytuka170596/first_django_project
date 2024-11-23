"""
Module that contains the views of the application Shopapp.
"""

from csv import DictWriter

from django.core.cache import cache
from django.db.models import QuerySet, Model, Field, CharField, TextField
from django.forms import ModelForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from shopapp.models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm, GroupForm
from .serializers import ProductSerializer, OrderSerializer

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from PIL import ImageFile
from typing import List, Tuple, Dict, Any, TypeVar, Optional
from timeit import default_timer
from .utils import save_csv_products

import logging


logger = logging.getLogger(__name__)
DjangoFilters = TypeVar("DjangoFilters")


class OrderViewSet(ModelViewSet):
    """
    A set of views for actions on the Order.
    Full CRUD for order entities.
    """

    queryset: QuerySet[Order] = Order.objects.all()
    serializer_class: ModelSerializer = OrderSerializer
    filter_backends: List[DjangoFilters] = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields: List[Field] = [
        "user__username",
        "user__id",
        "products__name",
        "products__id",
        "id",
        "delivery_address",
        "promocode",
        "created_at",
        "phone",
    ]
    filterset_fields: List[Field] = [
        "user__username",
        "user__id",
        "products__name",
        "products__id",
        "id",
        "delivery_address",
        "promocode",
        "created_at",
        "phone",
    ]
    ordering_field: List[Field] = [
        "user__username",
        "user__id",
        "products__name",
        "products__id",
        "id",
        "delivery_address",
        "promocode",
        "created_at",
        "phone",
    ]


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный CRUD для сущностей товара
    """

    queryset: QuerySet = Product.objects.all()
    serializer_class: ModelSerializer = ProductSerializer
    filter_backends: List[filter] = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields: List[Field] = [
        "created_by__username",
        "created_by__id",
        "name",
        "description",
    ]
    filterset_fields: List[Field] = [
        "created_by__username",
        "created_by__id",
        "id",
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields: List[Field] = [
        "id",
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one prodcut by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by ID not found"),
        },
    )
    def retrieve(self, *args, **kwargs) -> HttpResponse:
        return super().retrieve(*args, **kwargs)

    @action(methods=["GET"], detail=False)
    def download_csv(self, request: Request) -> HttpResponse:
        """Method for download csv file"""

        response = HttpResponse(content_type="text/csv")
        filename: str = "products-export.csv"
        response["Content-Description"]: str = f"attachment; filename={filename}"
        queryset: QuerySet = self.filter_queryset(self.get_queryset())
        fields: List[str] = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({field: getattr(product, field) for field in fields})

        return response

    @action(methods=["POST"], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request) -> Response:
        products = save_csv_products(
            file=request.FILES["file"].file, encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(data=serializer.data)


class ShopIndexView(View):
    """
    Приветственная страница.
    """

    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [("Монитор", 30000), ("Настольный ПК", 60000), ("Телефон", 20000)]

        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
        }
        logger.debug("Products for shop index: %s", products)
        logger.info("Rendering shop index")
        print("Shop index context:", context)
        return render(request, "shopapp/shop-index.html", context=context)


class GroupListView(View):
    """
    Список групп.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context: dict = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related("permissions").all(),
        }
        return render(
            request=request, template_name="shopapp/group-list.html", context=context
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form: ModelForm = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    """
    Подробности о товаре.
    """

    permission_required: Tuple[str] = ("shopapp.change_product",)
    template_name: str = "shopapp/products-details.html"
    model: Model = Product
    context_object_name: str = "product"


class ProductsListView(PermissionRequiredMixin, ListView):
    """
    Список товаров.
    """

    permission_required: Tuple[str] = ("shopapp.view_product",)
    template_name: str = "shopapp/products-list.html"
    # model = Product
    context_object_name: str = "products"
    queryset: QuerySet = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """
    Создание товара.
    """

    permission_required: Tuple[str] = ("shopapp.add_product",)

    model: Model = Product
    form_class: ModelForm = ProductForm
    # fields = "name", "price", "description", "discount", "preview"
    success_url: str = reverse_lazy("shopapp:products_list")

    def form_valid(self, form) -> None:
        form.instance.created_by = User.objects.get(id=self.request.user.pk)
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    """
    Обновление товара.
    """

    permission_required: Tuple[str] = ("shopapp.change_product",)
    model: Model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix: str = "_update_form"
    form_class: ModelForm = ProductForm

    def get_success_url(self) -> HttpResponse:
        return reverse("shopapp:product_details", kwargs={"pk": self.object.pk})

    def test_func(self) -> bool:
        self.object = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif (
            self.request.user.has_perm("shopapp.change_product")
            and self.object.created_by.pk == self.request.user.pk
        ):
            return True
        return False

    def form_valid(self, form) -> HttpResponse:
        form.instance.updated_by = User.objects.get(id=self.request.user.pk)
        response: HttpResponse = super().form_valid(form)

        # files = form.cleaned_data["file_field"]
        images_files: List[ImageFile] = form.FILES.getlist("images")
        for image in images_files:
            ProductImage.objects.create(product=self.object, image=image)
        return response


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Удаление товара.
    """

    permission_required: Tuple[str] = ("shopapp.delete_product",)
    # model = Product
    queryset: QuerySet = Product.objects.prefetch_related("images")
    success_url: str = reverse_lazy("shopapp:products_list")
    template_name_suffix: str = "_confirm_archive"

    def form_valid(self, form) -> HttpResponseRedirect:
        success_url: str = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    """
    Список заказов.
    """

    required_permissions: Tuple[str] = ("shopapp.view_order",)
    queryset: QuerySet = Order.objects.select_related("user").prefetch_related(
        "products"
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    """
    Подробности о заказе.
    """

    permission_required: Tuple[str] = "shopapp.view_order"
    template_name: str = "shopapp/order_details.html"
    queryset: QuerySet = Order.objects.select_related("user").prefetch_related(
        "products"
    )


class OrderCreateView(CreateView):
    """
    Создание заказа.
    """

    template_name: str = "shopapp/create-order.html"
    queryset: QuerySet = Order.objects.select_related("user").prefetch_related(
        "products"
    )
    form_class: ModelForm = OrderForm
    success_url: str = reverse_lazy("shopapp:orders_list")

    def get_success_url(self) -> HttpResponse:
        return reverse("shopapp:order_details", kwargs={"pk": self.object.pk})


class OrderUpdateView(UpdateView):
    """
    Обновление заказа.
    """

    model: Model = Order
    form_class: ModelForm = OrderForm
    template_name_suffix: str = "_update_form"
    success_url: str = reverse_lazy("shopapp:orders_list")


class OrderDeleteView(DeleteView):
    """
    Удаление заказа.
    """

    model: Model = Order
    success_url: str = reverse_lazy("shopapp:orders_list")
    template_name_suffix: str = "_confirm_delete"


class UserDetailsView(DetailView):
    """
    Просмотр информации о пользователе.
    """

    template_name: str = "shopapp/user-details.html"
    context_object_name: str = "user"
    model: Model = User


class ProductDataExportView(View):
    """
    Экспорт данных о товарах.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key: str = "products_data_export"
        products_data: List[Dict[str, Any]] = cache.get(cache_key)
        if products_data is None:
            products: QuerySet[Product] = Product.objects.order_by("pk").all()
            products_data: List[Dict[str, Any]] = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set("products_data_export", products_data, 300)
        return JsonResponse({"products": products_data})


class OrderDataExportView(UserPassesTestMixin, View):
    """
    Экспорт данных о заказах.
    """

    def test_func(self) -> bool:
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse | HttpResponse:
        orders: QuerySet[Order] = Order.objects.order_by("pk").all()
        orders_data: List[Dict[str, Any]] = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": [
                    product.pk for product in order.products.filter(archived=False)
                ],
            }
            for order in orders
        ]

        return JsonResponse({"orders": orders_data})


class LatestProductsFeed(Feed):
    """RSS feed for latest products."""

    title: str = "Latest product"
    description: str = (
        "The newest products, have time to evaluate before it's too late."
    )
    link: str = reverse_lazy("shopapp:products_list")

    def items(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(archived=False)
            .order_by("-created_at")
            .select_related("created_by")
        )

    def item_title(self, item: Product) -> CharField:
        """Returns the name of the product in RSS feed"""
        return item.name

    def item_description(self, item: Product) -> TextField:
        """Returns the description of the product, but within 300 characters"""
        return item.description[0:300]

    def item_link(self, item: Product) -> str:
        """Returns the link to the product in the RSS feed"""
        return reverse("shopapp:product_details", kwargs={"pk": item.pk})


class UserOrdersListView(UserPassesTestMixin, ListView):
    """List of user's orders"""

    def test_func(self) -> bool:
        return self.request.user.is_authenticated

    def get_queryset(self) -> QuerySet[Order]:
        user_pk: int = self.kwargs["pk"]
        self._owner: Optional[User] = get_object_or_404(User, pk=user_pk)
        queryset: QuerySet[Order] = Order.objects.select_related("user").filter(
            user__id=user_pk
        )
        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context_data: Dict[str, Any] = super().get_context_data(**kwargs)
        context_data["owner"] = self._owner
        return context_data


class UserOrderDataExportView(View):
    """Viewing for exporting a user's order by ID in json format"""

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user_pk: int = self.kwargs["pk"]
        cache_key: str = f"user_{user_pk}_orders_data_export"
        cached_data_orders: List[Dict[str, Any]] = cache.get(cache_key)
        if cached_data_orders is None:
            user: User = get_object_or_404(User, pk=user_pk)
            orders: QuerySet[Order] = Order.objects.filter(user=user).order_by("pk")
            serializer: OrderSerializer = OrderSerializer(instance=orders, many=True)
            cached_data_orders = serializer.data
            cache.set(cache_key, cached_data_orders, 180)

        return JsonResponse({"Orders": cached_data_orders})
