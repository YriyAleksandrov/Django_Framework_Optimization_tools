from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render


from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser  # вся работа будет производиться с классом ShopUser
    template_name = 'adminapp/user_create.html'  # на какой страничке
    context_object_name = 'user_form'  # что передаем
    success_url = reverse_lazy('admin_staff:users')  # реверс на какую страничку
    fields = ['username', 'first_name', 'last_name',
              'is_superuser', 'is_staff', 'is_active',
              'password', 'email', 'age', 'avatar']  # указываем поля для отображения

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователь/создание'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser  # вся работа будет производиться с классом ShopUser
    template_name = 'adminapp/user_update.html'  # на какой страничке
    context_object_name = 'user'  # что передаем
    success_url = reverse_lazy('admin_staff:users')  # реверс на какую страничку
    fields = ['username', 'first_name', 'last_name',
              'is_superuser', 'is_staff', 'is_active',  # указываем поля для отображения
              'password', 'email', 'age', 'avatar']     # fields = '__all__' - если надо указать все поля

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
#
# @user_passes_test(lambda x: x.is_superuser)
# def user_delete(request, pk):
#     user = get_object_or_404(get_user_model(), pk=pk)
#     if request.method == 'POST':
#         # user.is_active = False
#         user.delete()
#         # user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {
#         'title': 'пользователи/удаление',
#         'user_to_delete': user
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = ProductCategory  # вся работа будет производиться с классом ShopUser
    template_name = 'adminapp/category_update.html'  # на какой страничке
    context_object_name = 'edit_category'  # что передаем
    success_url = reverse_lazy('admin_staff:categories')  # реверс на какую страничку
    fields = '__all__'  # если надо указать все поля

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'adminapp/products.html'
#     context_object_name = 'objects'
#     form_class = ProductEditForm
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'админка/продукты'
#         return context
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукты'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category': category
    }

    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'
    category = get_object_or_404(ProductCategory, pk=pk)
    context = {
        'title': title,
        'object': category,
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    category = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        edit_form = ProductEditForm(instance=category)

    context = {
        'title': title,
        'product_form': edit_form,
        'object': category,
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'
    category = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.delete()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'object': category,
    }

    return render(request, 'adminapp/product_delete.html', context)
