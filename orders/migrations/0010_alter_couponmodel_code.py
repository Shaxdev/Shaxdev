# Generated by Django 3.2.9 on 2021-12-31 14:04

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_couponmodel_based_things'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponmodel',
            name='code',
            field=models.CharField(default=orders.models.generate_coupon_code, max_length=8, null=True),
        ),
    ]