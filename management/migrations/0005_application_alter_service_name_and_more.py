# Generated by Django 4.2.3 on 2023-08-04 20:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_citizenaddress_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('documentCategories', models.CharField(blank=True, choices=[('', 'Select Document Category'), ('None', 'None'), ('Ordinary Passport', 'Ordinary Passport'), ('Diplomatic Passport', 'Diplomatic Passport'), ('Service Passport', 'Service Passport')], default='', max_length=50, null=True, verbose_name='Document Category')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='application/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image')),
                ('status', models.BooleanField(blank=True, default=False, verbose_name='Status')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(choices=[('', 'Select Document Application'), ('e-Passport Application', 'e-Passport Application'), ('Individual Descriptive Document Application', 'Individual Descriptive Document Application')], default='', max_length=100, unique=True, verbose_name='Service Name'),
        ),
        migrations.DeleteModel(
            name='DocumentApplication',
        ),
        migrations.AddField(
            model_name='application',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.service', verbose_name='Service'),
        ),
    ]