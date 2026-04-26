from django.shortcuts import render
from .models import Item


def item(request, id):
    item = Item.objects.get(pk=id)
    data = {
        'title': 'Item',
        'item': item
    }
    return render(request, 'main/item.html', data)
