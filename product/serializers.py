from rest_framework import serializers
from .models import Category,Product,Review
from rest_framework.exceptions import ValidationError


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

class CategoryValidateSerialiser(serializers.Serializer):
    name = serializers.CharField(required=True,min_length=2,max_length=255)


class ProductValidateSerialiser(serializers.Serializer):
    title = serializers.CharField(required=True,min_length=2,max_length=255)
    description = serializers.CharField(required=False,default='No text')
    price = serializers.IntegerField()
    category = serializers.IntegerField()
    

    
    
    def validate_category(self, category):
        try:
            Category.objects.get(id=category)
        except Category.DoesNotExist: 
            raise ValidationError('Category does not exist! ')
        return category


class ReviewValidateSerialiser(serializers.Serializer):
    text = serializers.CharField()
    rating = serializers.IntegerField(required=True,min_value=1,max_value=10)
    product = serializers.IntegerField()


    def validate_product(self, product):
        try:
            Product.objects.get(id=product)
        except Product.DoesNotExist: 
            raise ValidationError('Product does not exist! ')
        return product
