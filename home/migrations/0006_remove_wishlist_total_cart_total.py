# Generated by Django 4.1.1 on 2022-10-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_wishlist_checkout_wishlist_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='total',
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
