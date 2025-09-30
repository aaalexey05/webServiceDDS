from django.db import models


class CashflowStatus(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self) -> str:
        return self.name


class CashflowType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    cf_type = models.ForeignKey(CashflowType, on_delete=models.PROTECT, related_name="categories")

    class Meta:
        unique_together = ("name", "cf_type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f"{self.name} ({self.cf_type})"


class Subcategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="subcategories")

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self) -> str:
        return f"{self.name} ↦ {self.category}"


class CashflowRecord(models.Model):
    created_at = models.DateField()
    status = models.ForeignKey(CashflowStatus, on_delete=models.PROTECT, related_name="records")
    cf_type = models.ForeignKey(CashflowType, on_delete=models.PROTECT, related_name="records")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="records")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="records")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "id"]
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"

    def __str__(self) -> str:
        return f"{self.created_at} {self.cf_type}/{self.category}/{self.subcategory}: {self.amount}₽"

    def clean(self):
        from .validators import (
            validate_category_belongs_to_type,
            validate_subcategory_belongs_to_category,
        )
        if self.category_id and self.cf_type_id:
            validate_category_belongs_to_type(self.category, self.cf_type)
        if self.subcategory_id and self.category_id:
            validate_subcategory_belongs_to_category(self.subcategory, self.category)

