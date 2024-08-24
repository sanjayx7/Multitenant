# In shop/admin.py

from django.contrib import admin
from .models import Brand, Category, Product

class ShopModelAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff and request.tenant.subscription_plan in ['premium', 'professional']

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff and request.tenant.subscription_plan in ['premium', 'professional']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff and request.tenant.subscription_plan == 'professional'

@admin.register(Brand)
class BrandAdmin(ShopModelAdmin):
    list_display = ('name',)  # Add other fields as needed

@admin.register(Category)
class CategoryAdmin(ShopModelAdmin):
    list_display = ('name',)  # Add other fields as needed

@admin.register(Product)
class ProductAdmin(ShopModelAdmin):
    list_display = ('name', 'category', 'brand')  # Add other fields as needed