from django.contrib import admin

from .models import (
    CashflowStatus,
    CashflowType,
    Category,
    Subcategory,
    CashflowRecord,
)


@admin.register(CashflowStatus)
class CashflowStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(CashflowType)
class CashflowTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cf_type")
    list_filter = ("cf_type",)
    search_fields = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(CashflowRecord)
class CashflowRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "status",
        "cf_type",
        "category",
        "subcategory",
        "amount",
    )
    list_filter = ("status", "cf_type", "category", "subcategory", "created_at")
    search_fields = ("comment",)
    date_hierarchy = "created_at"
