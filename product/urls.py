from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list),
    path('<int:id>/', views.category_detail),
    path('',views.product_list),
    path('<int:id>/', views.product_detail),
    path('',views.review_list),
    path('<int:id>/',views.review_detail),
]