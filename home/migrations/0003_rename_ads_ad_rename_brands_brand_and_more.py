# Generated by Django 4.1.1 on 2022-09-20 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_brand_brands_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ads',
            new_name='Ad',
        ),
        migrations.RenameModel(
            old_name='Brands',
            new_name='Brand',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='SubCategories',
            new_name='SubCategory',
        ),
    ]
