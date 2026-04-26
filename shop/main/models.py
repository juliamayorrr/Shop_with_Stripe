from decimal import Decimal
from django.db import models


class Item(models.Model):
    class Currency(models.TextChoices):
        dollar = 'usd'
        ruble = 'rub'

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(choices=Currency.choices, max_length=6)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    orders = models.ManyToManyField('Order', blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField('Item')
    currency = models.CharField(choices=Item.Currency.choices, max_length=6)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    discount = models.ForeignKey('Discount', related_name='orders',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey('Tax', related_name='orders',
                            on_delete=models.SET_NULL, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(blank=True, max_length=255)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'

    def calculate_total(self):
        total = sum(item.price for item in self.items.all())
        self.subtotal = total
        if self.discount and self.discount.percent_off:
            discount_amount = total * (self.discount.percent_off / Decimal('100'))
            total -= discount_amount
        if self.tax and self.tax.percent:
            tax_amount = total * (self.tax.percent / Decimal('100'))
            total += tax_amount
        self.amount = total.quantize(Decimal('0.01'))
        self.save(update_fields=['subtotal', 'amount'])
        return self.amount

    def get_stripe_amount(self):
        if self.amount:
            return int(self.amount * 100)
        else:
            return int(self.calculate_total() * 100)


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return self.name