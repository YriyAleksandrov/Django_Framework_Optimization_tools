from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):

    FORMING = 'FM'
    SENT_TO_PROCEED = 'SPT'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RD'
    CANCEL = 'CNC'
    DELIVERED = 'DVD'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Обработан'),
        (PAID, 'Оплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен'),
        (DELIVERED, 'Выдан'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default=FORMING, verbose_name='статус', max_length=3)
    is_active = models.BooleanField(default=True, verbose_name='активен')  # будет говорить, что пользователь хотел удалить наш заказ

# class OrderItemQuerySet(models.QuerySet):  # создаем менеджер объектов
#
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(OrderItemQuerySet, self).delete(*args, **kwargs)
    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return total_quantity

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        total_cost = sum(list(map(lambda x: x.get_product_cost(), items)))
        return total_cost

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quatity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):

    # objects = OrderItemQuerySet.as_manager()  # привязали менеджер объектов к модели

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return Order.objects.get(pk=pk)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)

