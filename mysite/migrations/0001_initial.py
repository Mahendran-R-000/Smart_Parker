# Generated by Django 5.0.2 on 2024-02-26 17:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Myusers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(default=' ', max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('total_transport', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('money_per_hour', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_money', models.CharField(default=0, max_length=300)),
                ('occupied_transport', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('latitude', models.CharField(blank=True, default=1, max_length=50, null=True)),
                ('longitude', models.CharField(blank=True, default=1, max_length=50, null=True)),
                ('hold', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(blank=True, upload_to='RentImages', verbose_name='Image')),
                ('rentuser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mysite.rentregister')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_name', models.CharField(default=' ', max_length=100)),
                ('vehicle', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('amount_to_pay', models.PositiveIntegerField(blank=True, null=True)),
                ('booked', models.BooleanField(default=False)),
                ('no_of_hours', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('booked_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('ending_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('booked_place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.rentregister')),
            ],
            options={
                'ordering': ['-booked_at'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=50)),
                ('transport_number', models.CharField(default=0, max_length=10)),
                ('description', models.TextField(max_length=450)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReportImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(blank=True, upload_to='ReportImages', verbose_name='report_images')),
                ('reportuser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mysite.report')),
            ],
        ),
        migrations.CreateModel(
            name='SlotsPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(default=' ', max_length=100)),
                ('slot_name', models.CharField(default=' ', max_length=100)),
                ('slot_available', models.BooleanField(default=True)),
                ('value', models.CharField(default='1', max_length=100)),
                ('edited', models.CharField(default='1', max_length=100)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-createdAt'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='', max_length=100)),
                ('phoneNumber', models.IntegerField(default=0)),
                ('reward_coins', models.IntegerField(default=0)),
                ('pincode', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, default='images.jpeg', upload_to='profile_image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=50)),
                ('vehicle_no', models.CharField(max_length=8, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]