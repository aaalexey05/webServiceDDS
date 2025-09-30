from django import forms
from datetime import date

from .models import CashflowRecord, Category, Subcategory


class CashflowRecordForm(forms.ModelForm):
    created_at = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = CashflowRecord
        fields = [
            "created_at",
            "status",
            "cf_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.initial.get("created_at") and not self.data.get("created_at"):
            self.fields["created_at"].initial = date.today()
        # Добавляем data-* для клиентской фильтрации списков
        self.fields["category"].queryset = Category.objects.select_related("cf_type").all()
        self.fields["subcategory"].queryset = Subcategory.objects.select_related("category").all()
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["subcategory"].widget.attrs.update({"class": "form-select"})
        self.fields["cf_type"].widget.attrs.update({"class": "form-select"})
        self.fields["status"].widget.attrs.update({"class": "form-select"})
        self.fields["amount"].widget.attrs.update({"class": "form-control", "step": "0.01"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "rows": 3})

        # Добавим data-* атрибуты в HTML через custom renderer: используем поле select и вручную сформируем options в шаблоне

    def clean_amount(self):
        from decimal import Decimal, InvalidOperation
        raw = self.cleaned_data.get("amount")
        if isinstance(raw, str):
            normalized = raw.replace(" ", "").replace("\u00A0", "").replace(",", ".")
            try:
                return Decimal(normalized)
            except InvalidOperation:
                raise forms.ValidationError("Введите сумму числом, например 1000.00")
        return raw


