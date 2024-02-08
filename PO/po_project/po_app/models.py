from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    left = models.IntegerField(null=False, blank=False)

class BasketState(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Basket(models.Model):
    total_price = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    state = models.ForeignKey(BasketState, on_delete=models.CASCADE, null=True, blank=True)

class StockInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=False, blank=False)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    number = models.IntegerField(default=0)

class Address(models.Model):
    city = models.CharField(max_length=255, null=False, blank=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    number = models.CharField(max_length=255, null=False, blank=False)

class DeliveryState(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Delivery(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=False)
    state = models.ForeignKey(DeliveryState, on_delete=models.CASCADE, null=False, blank=False)

class Bill(models.Model):
    receipt_number = models.CharField(max_length=255, null=False, blank=False)

class OrderState(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Order(models.Model):
    state = models.ForeignKey(OrderState, on_delete=models.CASCADE, null=False, blank=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=False, blank=False)
    date = models.CharField(max_length=255, null=False, blank=False)