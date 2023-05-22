import rest_framework.status
from django.db import transaction, IntegrityError
from django.http import HttpResponse

from .models import Product, Category, Order, OrderItem
from rest_framework import serializers, status
from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "amount", "photo", "category"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "amount"]


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "name", "email", "phone", "order_item"]


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "amount"]


class CreateOrderSerializer(serializers.ModelSerializer):
    order_item = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["name", "email", "phone", "order_item"]

    def create(self, validated_data):
        order_item_data = validated_data.pop("order_item")
        order = Order.objects.create(**validated_data)
        order_items = [OrderItem(order=order, **item) for item in order_item_data]
        product_ids = [item['product'].id for item in order_item_data]
        products = Product.objects.filter(id__in=product_ids)
        try:
            with transaction.atomic():
                for product, item in zip(products, order_item_data):
                    product.amount -= item['amount']

                Product.objects.bulk_update(products, ['amount'])
                OrderItem.objects.bulk_create(order_items)

        except IntegrityError:
            raise ValidationError(
                "requested amount bigger than available",
                code=status.HTTP_406_NOT_ACCEPTABLE
            )

        return order
