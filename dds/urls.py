from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CashflowStatusViewSet,
    CashflowTypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    CashflowRecordViewSet,
    record_list,
    record_create,
    record_update,
    record_delete,
)


router = DefaultRouter()
router.register(r'statuses', CashflowStatusViewSet)
router.register(r'types', CashflowTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'records', CashflowRecordViewSet)


urlpatterns = [
    path('', record_list, name='record-list'),
    path('records/new/', record_create, name='record-create'),
    path('records/<int:pk>/edit/', record_update, name='record-update'),
    path('records/<int:pk>/delete/', record_delete, name='record-delete'),
    path('api/', include(router.urls)),
]


