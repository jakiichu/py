from .views import index, Registation, Login, Products, ProductDetailView, AddToCart, CartView
from django.urls import path
from django.contrib.auth.views import LogoutView

app_name = 'BoardShop'

urlpatterns = [
    path('', index, name='index'),
    path('register/', Registation.as_view(), name='reg'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', Products, name='Product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='ProductView'),
    path('addToCart/<int:pk>/', AddToCart.as_view(), name='addToCart'),
    path('cart/', CartView.as_view(), name='cart')
]
