# myrestaurant/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nuts = models.BooleanField()
    image = models.URLField()
    vegetarian = models.BooleanField()
    spiciness = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Basket(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class BasketItem(models.Model):
    basket = models.ForeignKey('Basket', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='basket_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.basket.name}"