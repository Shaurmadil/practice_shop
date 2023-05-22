from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, CreateOrderSerializer


# Create your views here.


class ProductAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related("category")


class CategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class OrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related("order_item")


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = (AllowAny,)
