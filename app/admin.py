from django.contrib import admin
from . import models


@admin.register(models.Product)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', '_id', 'price', 'countInStock', 'rating', 'numReviews', 'createdAt', ) 
    search_fields = ('name',)


@admin.register(models.Order)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'createdAt', 'user', 'totalPrice', 'isPaid', 'paymentMethod', 'isDelivered') 
    search_fields = ('order_id',)
    

@admin.register(models.Review)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'user', 'comment') 
  

@admin.register(models.ShippingAddress)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('address', 'order', 'city', 'shippingPrice') 


@admin.register(models.OrderItem)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'qty', 'price', 'image') 
