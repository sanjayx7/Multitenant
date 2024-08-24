# Tenants/permissions.py

BASIC_PERMISSIONS = [
    'shop.view_brand',
    'shop.view_category',
    'shop.view_product',
    'auth.view_user',
    'auth.view_group',
]

PREMIUM_PERMISSIONS = BASIC_PERMISSIONS + [
    'shop.add_brand',
    'shop.change_brand',
    'shop.add_category',
    'shop.change_category',
    'shop.add_product',
    'shop.change_product',
]

PROFESSIONAL_PERMISSIONS = PREMIUM_PERMISSIONS + [
    'shop.delete_brand',
    'shop.delete_category',
    'shop.delete_product',
]