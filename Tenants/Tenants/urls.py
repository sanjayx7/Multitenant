from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shop/', include('api.v1.shop.urls')),  # Shop API URLs
    path('', include('Tenants.public_urls')),  # Add this line
]