from django.views.generic import View

from .models import Cart, User


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = User.objects.filter(id=request.user.id).first()
            # if not customer:
            #     customer = UserData.objects.create(
            #         user=request.user, id=request.user.id
            #     )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        # else:
        #     cart = Cart.objects.filter(for_anonymous_user=True, in_order=False).first()
        #     if not cart:
        #         cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
