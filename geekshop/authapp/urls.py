from django.urls import path
import authapp.views as authapp
from geekshop.views import main

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('profile/', authapp.edit, name='edit'),
    path('', main, name='main'),
    path('verify/<email>/<key>/', authapp.verify, name='verify')
]
