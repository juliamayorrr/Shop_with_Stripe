from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency']
    list_display_links = ['name']
    list_editable = ['price', 'currency']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent_off']
    list_display_links = ['name']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent']
    list_display_links = ['name']