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
        fields = ['title','description','price','category','product_count']

class ProductDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewListSerialiser(serializers.ModelSerializer):
     class Meta:
          model = Review 
          fields = ['text', 'product','rating']

class ReviewDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerialiser(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews']

class ProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model=Category
        fields=['id','name','products_count']





