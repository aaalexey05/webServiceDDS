from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import CashflowStatus, CashflowType, Category, Subcategory, CashflowRecord
from .serializers import (
    CashflowStatusSerializer,
    CashflowTypeSerializer,
    CategorySerializer,
    SubcategorySerializer,
    CashflowRecordSerializer,
)
from .forms import CashflowRecordForm


class CashflowStatusViewSet(viewsets.ModelViewSet):
    queryset = CashflowStatus.objects.all().order_by("name")
    serializer_class = CashflowStatusSerializer


class CashflowTypeViewSet(viewsets.ModelViewSet):
    queryset = CashflowType.objects.all().order_by("name")
    serializer_class = CashflowTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("cf_type").all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["cf_type"]


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.select_related("category", "category__cf_type").all().order_by("name")
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class CashflowRecordViewSet(viewsets.ModelViewSet):
    queryset = (
        CashflowRecord.objects.select_related(
            "status", "cf_type", "category", "subcategory"
        ).all()
    )
    serializer_class = CashflowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "created_at": ["gte", "lte"],
        "status": ["exact"],
        "cf_type": ["exact"],
        "category": ["exact"],
        "subcategory": ["exact"],
    }

def record_list(request):
    qs = CashflowRecord.objects.select_related(
        "status", "cf_type", "category", "subcategory"
    ).all()
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status_id = request.GET.get("status")
    type_id = request.GET.get("cf_type")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    if date_from:
        qs = qs.filter(created_at__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__lte=date_to)
    if status_id:
        qs = qs.filter(status_id=status_id)
    if type_id:
        qs = qs.filter(cf_type_id=type_id)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if subcategory_id:
        qs = qs.filter(subcategory_id=subcategory_id)

    qs = qs.order_by("-created_at", "id")
    totals = qs.aggregate(total_amount=Sum("amount"))
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "records": page_obj.object_list,
        "page_obj": page_obj,
        "total_amount": totals.get("total_amount") or 0,
        "statuses": CashflowStatus.objects.all(),
        "types": CashflowType.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": Subcategory.objects.all(),
    }
    return render(request, "dds/record_list.html", context)


def record_create(request):
    if request.method == "POST":
        form = CashflowRecordForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.full_clean()
            instance.save()
            return redirect(reverse("record-list"))
    else:
        form = CashflowRecordForm()
    return render(request, "dds/record_form.html", {"form": form})


def record_update(request, pk: int):
    obj = get_object_or_404(CashflowRecord, pk=pk)
    if request.method == "POST":
        form = CashflowRecordForm(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.full_clean()
            instance.save()
            return redirect(reverse("record-list"))
    else:
        form = CashflowRecordForm(instance=obj)
    return render(request, "dds/record_form.html", {"form": form, "object": obj})


def record_delete(request, pk: int):
    obj = get_object_or_404(CashflowRecord, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(reverse("record-list"))
    return render(request, "dds/confirm_delete.html", {"object": obj})


# Create your views here.
