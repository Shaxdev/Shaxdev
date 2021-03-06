# Generated by Django 3.2.9 on 2021-12-18 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Default_avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='static/images/pictures/avatars')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'default user avatar',
                'verbose_name_plural': 'default user avatars',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(blank=True, default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.zooniverse.org%2Fprojects%2Fpenguintom79%2Fpenguin-watch&psig=AOvVaw3znYM4x-Z6U1aNeuECcWYg&ust=1639545794567000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCPjdrsbG4vQCFQAAAAAdAAAAABAH', null=True, upload_to='static/images/pictures/profiles')),
                ('username', models.CharField(help_text='username', max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('zip', models.IntegerField(help_text='enter your pochta code')),
                ('phone', models.CharField(help_text='example:  +998991547854', max_length=20)),
            ],
            options={
                'verbose_name': 'User_information',
                'verbose_name_plural': 'User_informations',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('street', models.CharField(max_length=80)),
                ('building', models.CharField(blank=True, max_length=60, null=True)),
                ('apartment', models.CharField(blank=True, max_length=12, null=True)),
                ('floor', models.CharField(blank=True, max_length=4, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User_address',
                'verbose_name_plural': 'User_addresses',
            },
        ),
    ]
