# Generated by Django 4.0.2 on 2022-04-23 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_product_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='items_json',
        ),
    ]
