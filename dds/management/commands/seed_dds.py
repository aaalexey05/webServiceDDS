from django.core.management.base import BaseCommand

from dds.models import CashflowStatus, CashflowType, Category, Subcategory


class Command(BaseCommand):
    help = "Загрузить базовые справочники ДДС"

    def handle(self, *args, **options):
        statuses = ["Бизнес", "Личное", "Налог"]
        for name in statuses:
            CashflowStatus.objects.get_or_create(name=name)

        types = ["Пополнение", "Списание"]
        type_map = {}
        for name in types:
            t, _ = CashflowType.objects.get_or_create(name=name)
            type_map[name] = t

        infra = Category.objects.get_or_create(name="Инфраструктура", cf_type=type_map["Списание"])[0]
        marketing = Category.objects.get_or_create(name="Маркетинг", cf_type=type_map["Списание"])[0]

        Subcategory.objects.get_or_create(name="VPS", category=infra)
        Subcategory.objects.get_or_create(name="Proxy", category=infra)
        Subcategory.objects.get_or_create(name="Farpost", category=marketing)
        Subcategory.objects.get_or_create(name="Avito", category=marketing)

        self.stdout.write(self.style.SUCCESS("Справочники загружены"))
