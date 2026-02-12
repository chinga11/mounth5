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


@api_view(http_method_names=['GET','POST'])
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.prefetch_related('product_set__reviews').all()
        data = CategoryListSerialiser(instance=category, many=True).data
        
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerialiser(category).data)

@api_view(['GET','PUT','DELETE'])
def category_detail(request,id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error':'category not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerialiser(category,many=False).data
        return Response(data=data)
    elif request.method =='PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,data=CategoryDetailSerialiser(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        product = (Product.objects.select_related('category').prefetch_related('reviews').all())

        data = ProductListSerialiser(instance=product, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
    )
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')
        product_count = request.data.get('product_count')

        product = Product.objects.create(
            title = title,
            description = description,
            price = price,
            category =category,
            product_count = product_count,
    )
    product.save()

    return Response(status=status.HTTP_201_CREATED,data=ProductDetailSerialiser(product).data)

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error':'product not found'})
    if request.method == 'GET':
        data = ProductDetailSerialiser(product,many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category = request.data.get('category')
        product.product_count = request.data.get('product_count')
        product.save()
        return Response(status=status.HTTP_201_CREATED,data=ProductDetailSerialiser(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(http_method_names=['GET','POST'])
def review_list(request):
    if request.method == 'GET':
        review = (Review.objects.select_related('product__category').all())
        data = ReviewListSerialiser(instance=review, many= True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
    )

    elif request.method == 'POST':
        text = request.data.get('text')
        rating = request.data.get('rating')
        product = request.data.get('product')
        
        review = Review.objects.create(
            text = text,
            rating = rating,
            product = product,
    )
        review.save()
        return Response(status=status.HTTP_201_CREATED,data = ReviewDetailSerialiser(review).data)
    
@api_view(['GET','PUT','DELETE'])
def review_detail(request,id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error':'review not found'})
    if request.method == 'GET':
        data = ReviewDetailSerialiser(review,many=False).data
        return Response(
            status=status.HTTP_200_OK,
            data=data)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.rating = request.data.get('rating')
        review.product = request.data.get('product')
        review.save()
        return Response(status=status.HTTP_201_CREATED,data=ReviewDetailSerialiser(review).data)
    elif request.method == 'DELETE':
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