# Generated by Django 4.0.2 on 2022-04-22 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_orderupdate_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
    ]
