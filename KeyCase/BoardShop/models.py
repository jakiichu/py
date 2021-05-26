from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
# Create your models here.


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=299)
    img = models.ImageField(upload_to='static/img/content', validators=[
                            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    # validators=[FileExtensionValidator(allowed_extensions=['png']), validate_image]

    def __str__(self):
        return self.name


class CartProduct(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return 'Товар: {}, кол-во: {}'.format(self.product.name, self.qty)
    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    final_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    # for_anonymous_user = models.BooleanField(default=False)
    qty = models.PositiveIntegerField(default=0)
