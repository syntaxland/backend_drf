from django.contrib import admin
from . import models


@admin.register(models.Product)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', '_id', 'price', 'countInStock', 'rating', 'numReviews', 'createdAt', ) 


@admin.register(models.Order)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('createdAt', 'order_id', '_id', 'user', 'totalPrice', 'isPaid', 'paymentMethod', 'isDelivered') 
    

@admin.register(models.Review)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'user', 'comment') 
  

@admin.register(models.ShippingAddress)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('address', 'order', 'city', 'shippingPrice') 


admin.site.register(models.OrderItem)
