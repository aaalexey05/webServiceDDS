from django import template

register = template.Library()


@register.filter
def rub(value):
    try:
        s = f"{value:,.2f}".replace(",", " ")
        return f"{s} ₽"
    except Exception:
        return value


