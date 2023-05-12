from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank="True")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="product", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class Order(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    amount = models.PositiveIntegerField()
