from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category,Product,Review
from django.db.models import Avg
from .serializers import CategoryListSerialiser,ProductListSerialiser,ReviewListSerialiser,CategoryDetailSerialiser,ProductDetailSerialiser,ReviewDetailSerialiser
from .serializers import ProductWithReviewsSerializer,ProductCountSerializer
from .serializers import CategoryValidateSerialiser,ProductValidateSerialiser,ReviewValidateSerialiser
from django.db import transaction
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.generics import ListAPIView
from django.http import Http404
from common.permissions import IsOwner,IsAnonymous

class CategoryListView(APIView):
    def get(self,request):
        category = Category.objects.prefetch_related('product_set__reviews').all()
        data = CategoryListSerialiser(instance=category, many=True).data
        
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    def post(self,request):
        serialiser = CategoryValidateSerialiser(data=request.data)
        if not serialiser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serialiser.errors)

        name = serialiser.validated_data.get('name')
        with transaction.atomic():
            category = Category.objects.create(
                name=name
            )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerialiser(category).data)

class CategoryDetailView(APIView):
    
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self,request,id):
        category = self.get_object(id)
        data = CategoryDetailSerialiser(category,many=False).data
        return Response(data=data)
    def put(self,request,id):
        category = self.get_object(id)
        serialiser = CategoryValidateSerialiser(data=request.data)
        serialiser.is_valid(raise_exception=True)
        category.name = serialiser.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK,data=CategoryDetailSerialiser(category).data)
    def delete(self,request,id):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListView(APIView):
    permission_classes = (IsOwner | IsAnonymous,)
    def get(self,request):
        product = (Product.objects.select_related('category').prefetch_related('reviews').all())

        data = ProductListSerialiser(instance=product, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
    )
    def post(self,request):
        serializer = ProductValidateSerialiser(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category = serializer.validated_data.get('category')
        product_count = serializer.validated_data.get('product_count')
        with transaction.atomic():
            product = Product.objects.create(
                title = title,
                description = description,
                price = price,
                category =category,
                product_count = product_count,
        )
            product.save()

        return Response(status=status.HTTP_201_CREATED,data=ProductDetailSerialiser(product).data)

class ProductDetailView(APIView):
    permission_classes = [IsOwner]
    def get_object(self,id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
    def get(self,request,id):
        product = self.get_object(id)
        data = ProductDetailSerialiser(product,many=False).data
        return Response(data=data)
    def put(self,request,id):
        product = self.get_object(id)
        serialiser = ProductValidateSerialiser(data=request.data)
        serialiser.is_valid(raise_exception=True)
        product.title = serialiser.validated_data.get('title')
        product.description = serialiser.validated_data.get('description')
        product.price = serialiser.validated_data.get('price')
        product.category = serialiser.validated_data.get('category')
        product.product_count = serialiser.validated_data.get('product_count')
        product.save()
        return Response(status=status.HTTP_200_OK,data=ProductDetailSerialiser(product).data)
    def delete(self,request,id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewListView(APIView):
    def get(self,request):
        review = (Review.objects.select_related('product__category').all())
        data = ReviewListSerialiser(instance=review, many= True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
    )

    def post(self,request):
        serialiser = ReviewValidateSerialiser(data=request.data)
        if not serialiser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serialiser.errors)
        text = serialiser.validated_data.get('text')
        rating = serialiser.validated_data.get('rating')
        product = serialiser.validated_data.get('product')
        with transaction.atomic():
            review = Review.objects.create(
                text = text,
                rating = rating,
                product = product,
        )
            review.save()
        return Response(status=status.HTTP_201_CREATED,data = ReviewDetailSerialiser(review).data)
    
class ReviewDetailView(APIView):
    def get_object(self,id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            raise Http404
    def get (self,request,id):
        review = self.get_object(id)
        data = ReviewDetailSerialiser(review,many=False).data
        return Response(
            status=status.HTTP_200_OK,
            data=data)
    def put(self,request,id):
        review = self.get_object(id)
        serializer = ReviewValidateSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.rating = serializer.validated_data.get('rating')
        review.product = serializer.validated_data.get('product')
        review.save()
        return Response(status=status.HTTP_200_OK,data=ReviewDetailSerialiser(review).data)
    def delete(self,request,id):
        review = self.get_object(id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductsReviewsView(APIView):
    def get(self, request):
        products = Product.objects.all().prefetch_related('reviews')
        serializer = ProductWithReviewsSerializer(products, many=True)

        
        global_avg_rating = Review.objects.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0

        return Response({
            "global_average_rating": global_avg_rating,
            "products": serializer.data
        })
    

class ProductCountAPIView(ListAPIView):
    serializer_class = ProductCountSerializer


    def get_queryset(self):
        return Category.objects.annotate(
            products_count=Count('product')
        )