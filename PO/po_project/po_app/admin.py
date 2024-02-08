from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Stock)
admin.site.register(BasketState)
admin.site.register(Basket)
admin.site.register(StockInBasket)
admin.site.register(Address)
admin.site.register(DeliveryState)
admin.site.register(Delivery)
admin.site.register(Bill)
admin.site.register(OrderState)
admin.site.register(Order)