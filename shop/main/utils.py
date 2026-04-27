from main.models import Order


def get_active_order(request):
    """Возвращает активную корзину или None"""

    order_id = request.session.get('order_id')
    if not order_id:
        return None

    order = Order.objects.filter(pk=order_id, status=Order.Status.CART).first()
    if not order:
        del request.session['order_id']
        return None

    return order