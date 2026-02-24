from django.urls import path
from . import views
from .views import (
    CategoryDetailView,
    CategoryListView,
    ProductListView,
    ProductDetailView,
    ReviewListView,
    ReviewDetailView,
)
urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:id>/', CategoryDetailView.as_view()),
    path('',ProductListView.as_view()),
    path('<int:id>/', ProductDetailView.as_view()),
    path('', ReviewListView.as_view()),
    path('<int:id>/',ReviewDetailView.as_view()),
]