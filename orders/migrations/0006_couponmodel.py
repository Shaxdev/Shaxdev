# Generated by Django 3.2.9 on 2021-12-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0005_auto_20211229_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('expiration_time', models.DateTimeField(null=True)),
                ('based_things', models.ManyToManyField(null=True, to='products.SubcategoryModel', verbose_name='Coupon based these things')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
    ]