# Generated by Django 3.2.9 on 2021-12-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('All of good', 'All of good'), ('Return', 'Return'), ('Cancel', 'Cancel')], default='All of good', max_length=20, null=True),
        ),
    ]
