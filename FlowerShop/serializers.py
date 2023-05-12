from .models import Product, Category, Order, OrderItem
from rest_framework import serializers


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

        for item in order_item_data:
            OrderItem.objects.create(order=order, **item)

        return order