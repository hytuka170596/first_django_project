"""
Module for registering admins for the application/site
"""

from django.urls import path
from http.client import HTTPResponse

from django.db.models import Model
from typing import List, Tuple, Optional
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin

from .forms import CSVImportForm, JSONImportForm
from typing import Dict
from .utils import save_csv_products, save_json_orders


class OrderInline(admin.TabularInline):
    """Inline for Order model in ProductAdmin."""

    model: Model = Product.orders.through


class ProductImageInline(admin.StackedInline):
    model: Model = ProductImage


@admin.action(description="Archived products")
def make_archived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
):
    """Action to archive products."""
    queryset.update(archived=True)


@admin.action(description="Unarchived products")
def make_unarchived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
):
    """Action to un archive products."""
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    """Admin for Product model."""

    change_list_template = "shopapp/products_changelist.html"

    actions: List[str] = [
        make_archived,
        make_unarchived,
        "export_csv",
    ]
    inlines: List[admin.TabularInline] = [OrderInline, ProductImageInline]
    list_display: List[str] = (
        "pk",
        "name",
        "description_short",
        "price",
        "discount",
        "archived",
        "final_price",
    )
    list_display_links: Tuple[str] = "pk", "name"
    ordering: Tuple[str] = ("pk",)
    search_fields: Tuple[str] = "name", "description"
    fieldsets: List[tuple[str, dict]] = [
        (None, {"fields": ("name", "description")}),
        (
            "Price options",
            {"fields": ("price", "discount"), "classes": ("collapse", "wide")},
        ),
        (
            "Images",
            {
                "fields": ("preview",),
                # "classes": ("collapse", "wide"),
            },
        ),
        ("Extra options", {"fields": ("archived",), "classes": ("collapse",)}),
    ]

    def import_csv(self, request: HttpRequest) -> HTTPResponse:
        """Method for importing CSV file."""
        if request.method == "GET":
            form: CSVImportForm = CSVImportForm()
            context: Dict[str, Optional[CSVImportForm]] = {
                "form": form,
            }
            return render(
                request=request, template_name="admin/csv_form.html", context=context
            )
        form: CSVImportForm = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context: Dict[str, Optional[CSVImportForm]] = {
                "form": form,
            }
            return render(
                request=request,
                template_name="admin/csv_form.html",
                context=context,
                status=400,
            )
        save_csv_products(
            csv_file=form.cleaned_data["csv_file"].file, encoding=request.encoding
        )

        self.message_user(request=request, message="Data from CSV was imported.")
        return redirect(to="..")

    def get_urls(self) -> List[path]:
        urls: List[path] = super().get_urls()
        new_urls: List[path] = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            )
        ]
        return new_urls + urls


class ProductInline(admin.StackedInline):
    """Inline for Product model in OrderAdmin."""

    model: Model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Order model instances.
    """

    change_list_template: str = "shopapp/orders_changelist.html"
    """Template for the change list view of orders."""

    inlines: List[admin.StackedInline] = [
        ProductInline,
    ]
    list_display: Tuple[str] = (
        "delivery_address",
        "promocode",
        "created_at",
        "user_verbose",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Order]:
        """Return queryset with prefetched related fields."""
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        """Return verbose representation of user."""
        return obj.user.first_name or obj.user.username

    def import_json(self, request: HttpRequest) -> HTTPResponse:
        """Method for importing JSON file."""
        if request.method == "GET":
            json_form: JSONImportForm = JSONImportForm()
            context: Dict[str, Optional[JSONImportForm]] = {
                "form": json_form,
            }
            return render(
                request=request, template_name="admin/json_form.html", context=context
            )
        json_form: JSONImportForm = JSONImportForm(request.POST, request.FILES)

        if not json_form.is_valid():
            context: Dict[str, Optional[JSONImportForm]] = {
                "form": json_form,
            }
            return render(
                request=request,
                template_name="admin/json_form.html",
                context=context,
                status=400,
            )
        try:
            json_file = json_form.cleaned_data["json_file"]
            json_file.seek(0)
            added_file = save_json_orders(
                json_file=json_form.cleaned_data["json_file"],
                encoding=request.encoding,
            )

            if isinstance(added_file, str):
                message_error: str = added_file
                self.message_user(
                    request=request,
                    message=message_error,
                )

            self.message_user(
                request=request,
                message="The data from the form has been successfully added",
            )
            return redirect(to="..")
        except Exception as error:
            self.message_user(
                request,
                f"Error saving orders: {str(error)}",
                level="error",
            )
            return redirect(to="..")

    def get_urls(self) -> List[path]:
        """Get the URLs for the admin interface, including custom URLs."""
        urls: List[path] = super().get_urls()
        new_urls: List[path] = [
            path(
                "import-orders-json/",
                self.import_json,
                name="import_orders_json",
            )
        ]
        return new_urls + urls
