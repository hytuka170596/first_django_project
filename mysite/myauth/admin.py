from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bio",
        "sex",
        "agreement_accepted",
        "created_at",
        "avatar",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "sex",
        "user",
        "bio",
        "agreement_accepted",
        "created_at",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "bio",
        "agreement_accepted",
        "created_at",
        "avatar",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-pk",)
    list_per_page = 20
