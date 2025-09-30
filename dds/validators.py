from django.core.exceptions import ValidationError


def validate_category_belongs_to_type(category, cf_type):
    if category.cf_type_id != cf_type.id:
        raise ValidationError("Категория не относится к выбранному типу.")


def validate_subcategory_belongs_to_category(subcategory, category):
    if subcategory.category_id != category.id:
        raise ValidationError("Подкатегория не относится к выбранной категории.")


