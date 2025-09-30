from rest_framework import serializers

from .models import CashflowStatus, CashflowType, Category, Subcategory, CashflowRecord


class CashflowStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowStatus
        fields = ["id", "name"]


class CashflowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowType
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "cf_type"]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]


class CashflowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowRecord
        fields = [
            "id",
            "created_at",
            "status",
            "cf_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        instance = CashflowRecord(**attrs)
        instance.clean()
        return attrs


