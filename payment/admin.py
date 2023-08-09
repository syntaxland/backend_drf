from django.contrib import admin
from . import models


@admin.register(models.Payment)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'order_id','amount', 'reference',  )

    def first_name(self, obj):
        return obj.user.first_name

    first_name.short_description = 'First Name'
