"""
Admin mixins for the admin site.
Converts CSV to JSON and vice versa.
"""

import csv

from django.db.models.options import Options
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse


class ExportAsCSVMixin:
    """Mixin for exporting queryset as CSV."""

    def export_csv(self, request: HttpRequest, queryset: QuerySet) -> HttpResponse:
        """Export queryset as CSV."""
        meta: Options = self.model._meta
        field_names: list[str] = [field.name for field in meta.fields]

        response: HttpResponse = HttpResponse(content_type="text/csv")
        response["Content-Description"]: str = f"attachment; filename={meta}-export.csv"

        csv_writer: csv.writer = csv.writer(response)
        csv_writer.writerow(field_names)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_csv.short_description = "Export as CSV"
