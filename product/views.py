from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category,Product,Review
from django.db.models import Avg
from .serializers import CategoryListSerialiser,ProductListSerialiser,ReviewListSerialiser,CategoryDetailSerialiser,ProductDetailSerialiser,ReviewDetailSerialiser
from .serializers import ProductWithReviewsSerializer,ProductCountSerializer
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.generics import ListAPIView


@api_view(http_method_names=['GET'])
def category_list(request):
    category = Category.objects.all()
    data = CategoryListSerialiser(instance=category, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )


@api_view(['GET'])
def category_detail(request,id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error':'category not found'})
    data = CategoryDetailSerialiser(category,many=False).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def product_list(request):
    product = Product.objects.all()
    data = ProductListSerialiser(instance=product, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(['GET'])
def product_detail(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error':'product not found'})
    data = ProductDetailSerialiser(product,many=False).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_list(request):
    review = Review.objects.all()
    data = ReviewListSerialiser(instance=review, many= True).data
    return Response(
     status=status.HTTP_200_OK,
     data=data

    )

@api_view(['GET'])
def review_detail(request,id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error':'review not found'})
    data = ReviewDetailSerialiser(review,many=False).data
    return Response(
        status=status.HTTP_200_OK,
        data=data)




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