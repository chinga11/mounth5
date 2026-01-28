from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category,Product,Review
from .serializers import CategoryListSerialiser,ProductListSerialiser,ReviewListSerialiser,CategoryDetailSerialiser,ProductDetailSerialiser,ReviewDetailSerialiser


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
