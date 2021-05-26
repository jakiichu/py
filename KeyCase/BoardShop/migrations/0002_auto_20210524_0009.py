# Generated by Django 3.2.3 on 2021-05-23 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoardShop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=299, max_digits=12),
        ),
    ]
