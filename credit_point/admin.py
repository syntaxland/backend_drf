from django.contrib import admin
from . import models


@admin.register(models.CreditPointRequest)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'account_name', 'account_number', 
                    'bank_name', 'credit_point_amount', 'is_paid', 'paid_at',
                    'is_delivered', 'delivered_at',)
    search_fields = ('account_number', 'user')  

