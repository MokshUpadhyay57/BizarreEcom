# Generated by Django 4.0.2 on 2022-04-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_orders_items_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='update_desc',
            field=models.CharField(default='Order has been placed', max_length=5000),
        ),
    ]
