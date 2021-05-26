from django.shortcuts import render
from django.views import generic
from .models import User, Product, CartProduct
from .forms import RegitrationsForm
from .mixins import CartMixin
from .utils import recalc_cart
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
# КТО Я
# АСКА ТУПО ЛУЧШЕ


def index(request):
    # count = Product.aggregate(count=Count('id'))['count']
    # random_index = randint(0, count - 1)
    # randBoard = Product.objects.all()
    model = Product.objects.order_by('?')[:3]
    return render(request, 'index.html', {'rand': model})


def Products(request):
    model = Product.objects.all()
    return render(request, 'products.html', {'products': model})


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'

class AddToCart(CartMixin, generic.View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs.get('pk'))
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product, price=product.price
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            productQTY = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, product=product, price=product.price
            )
            productQTY.qty += 1
            productQTY.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect(reverse('BoardShop:ProductView', args=[kwargs.get('pk')]))

class CartView(CartMixin, generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cart.html', {'cart': self.cart})

class Login(LoginView):
    template_name = 'login.html'

    def get_redirect_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return '/admin'
        else:
            return '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('BoardShop:index'))
        return super().get(request, *args, **kwargs)


class Registation(generic.CreateView):
    template_name = 'registration.html'
    model = User
    form_class = RegitrationsForm
    success_url = reverse_lazy('BoardShop:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('BoardShop:index'))
        return super().get(request, *args, **kwargs)


