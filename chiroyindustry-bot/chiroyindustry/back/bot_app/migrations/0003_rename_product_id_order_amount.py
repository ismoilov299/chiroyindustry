# Generated by Django 5.0.3 on 2024-04-03 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0002_remove_product_category_remove_orderproduct_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product_id',
            new_name='amount',
        ),
    ]