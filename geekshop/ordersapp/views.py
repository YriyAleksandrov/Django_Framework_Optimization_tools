from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from ordersapp.forms import OrderItemEditForm, OrderEditForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):  # создаем только те заказы, которые принадлежат пользователю
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    success_url = reverse_lazy('order:list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = list(Basket.objects.filter(user=self.request.user))  # взяли всё что есть у юзера в корзине
            if len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemEditForm, extra=len(basket_items)
                )
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    basket_items[num].delete()
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # проверка, если пустые заказы, то произойдет откат выполненных действий
            form.instance.user = self.request.user  # задали дефолтное значение у юзера
            self.object = form.save()  # self.object - старая форма : form.save() - полученная новая форма
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:  # проверка, если создан заказ с количеством 0, то удаляем заказ
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    success_url = reverse_lazy('order:list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            orderitems_formset = OrderFormSet(instance=self.object)
            for form in orderitems_formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = orderitems_formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # проверка, если пустые заказы, то произойдет откат выполненных действий
            form.instance.user = self.request.user  # задали дефолтное значение у юзера
            self.object = form.save()  # self.object - старая форма : form.save() - полученная новая форма
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:  # проверка, если создан заказ с количеством 0, то удаляем заказ
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')


class OrderRead(DetailView):
    model = Order


def forming_complete(request, pk):  # статус из "формируется" меняется на "отправлен в обработку"
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:list'))


@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def products_quantity_update_save(sender, update_fields, instance, **kwargs):
    # if 'product' in update_fields or 'quantity' in update_fields:
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def products_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def payment_result(request):
    # ik_inv_st=success
    # ik_pm_no=ID
    payment_status = request.GET.get('ik_inv_st')
    if payment_status == 'success':
        order_pk = request.GET.get('ik_pm_no').replace('ID', '')
        order_item = Order.objects.get(pk=order_pk)
        order_item.status = Order.PAID
        order_item.save()
    return HttpResponseRedirect(reverse('order:list'))


