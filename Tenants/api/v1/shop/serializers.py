# shop/serializers.py
from rest_framework import serializers
from shop.models import Brand, Category, Product

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name','description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()  # Nested BrandSerializer
    category = CategorySerializer()  # Nested CategorySerializer

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'category', 'price', 'stock']