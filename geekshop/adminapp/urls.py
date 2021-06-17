import adminapp.views as adminapp
from django.urls import path
from geekshop.views import main

app_name = 'adminapp'

urlpatterns = [
    path('', main, name='main'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    # path('users/read/', adminapp.users, name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    # path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    # path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    # path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories'),
    # path('categories/read/', adminapp.categories, name='categories'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    # path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    # path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),
    # path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    # path('products/read/category/<int:pk>/', adminapp.ProductDetailView.as_view(), name='products'),
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]
