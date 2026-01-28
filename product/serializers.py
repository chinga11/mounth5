from rest_framework import serializers
from .models import Category,Product,Review


class CategoryListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CategoryDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description','price','category']

class ProductDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewListSerialiser(serializers.ModelSerializer):
     class Meta:
          model = Review 
          fields = ['text', 'product']

class ReviewDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'