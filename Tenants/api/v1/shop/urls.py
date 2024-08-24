# shop/urls.py
from django.urls import path
from api.v1.shop.views import (
    BrandList,
    BrandDetail,
    CategoryList,
    CategoryDetail,
    ProductList,
    ProductDetail,

)

urlpatterns = [

    path('brands/', BrandList.as_view(), name='brand-list'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='brand-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]
#celery -A tenants worker --loglevel=info


