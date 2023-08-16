from django.contrib import admin
from . import models


@admin.register(models.Payment)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'order_id', 'amount', 'reference',)
    search_fields = ('order_id', 'reference', 'email') 

    # def first_name(self, obj):
    #     return obj.user.first_name

    # def phone_number(self, obj):
    #     return obj.user.phone_number
    
    # def email(self, obj):
    #     return obj.user.email

    # first_name.short_description = 'First Name'
    # phone_number.short_description = 'Phone Number'
