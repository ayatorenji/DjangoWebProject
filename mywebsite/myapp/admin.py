from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(contactList)
admin.site.register(Profile)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'status', 'submitted']
    list_filter = ['submitted', 'status']
    search_fields = ['user__username', 'product__title']