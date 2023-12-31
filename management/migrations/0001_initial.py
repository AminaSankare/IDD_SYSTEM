# Generated by Django 4.2.3 on 2023-07-22 07:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], default='', max_length=10, verbose_name='Gender')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('birth_place', models.CharField(max_length=100, verbose_name='Birth place')),
                ('marital_status', models.CharField(choices=[('', 'Select Marital'), ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Separated', 'Separated'), ('Widowed', 'Widowed')], default='', max_length=20, verbose_name='Marital Status')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationality')),
                ('nid_number', models.CharField(max_length=50, unique=True, verbose_name='National ID Number')),
                ('createdDate', models.DateField(auto_now_add=True, verbose_name='Created Date')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Service Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('processingTime', models.CharField(max_length=50, verbose_name='Processing Time')),
                ('fees', models.CharField(max_length=100, verbose_name='Fees')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('document', models.CharField(choices=[('', 'Select Document'), ('Passport', 'Passport'), ('Individual Descriptive Document', 'Individual Descriptive Document')], default='', max_length=50, verbose_name='Document Requesting')),
                ('documentCategories', models.CharField(blank=True, choices=[('', 'Select Document Category'), ('None', 'None'), ('Ordinary Passport', 'Ordinary Passport'), ('Diplomatic Passport', 'Diplomatic Passport'), ('Service Passport', 'Service Passport')], default='', max_length=50, null=True, verbose_name='Document Category')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='application/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image')),
                ('status', models.IntegerField(blank=True, default=False, verbose_name='Status')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.CreateModel(
            name='CitizenParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(choices=[('', 'Select Parent'), ('Father', 'Father'), ('Mother', 'Mother')], default='', max_length=10, verbose_name='Parent')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
                ('professionalism', models.CharField(blank=True, max_length=50, verbose_name='Professionalism')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.CreateModel(
            name='CitizenDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(choices=[('', 'Select Document'), ('Passport', 'Passport'), ('Individual Descriptive Document', 'Individual Descriptive Document')], default='', max_length=50, verbose_name='Document')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='citizens/documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Image')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.CreateModel(
            name='CitizenAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50, verbose_name='Province')),
                ('state', models.CharField(max_length=50, verbose_name='State')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('street', models.CharField(max_length=50, verbose_name='Street')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
    ]
