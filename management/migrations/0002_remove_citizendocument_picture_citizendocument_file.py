# Generated by Django 4.2.3 on 2023-07-22 22:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizendocument',
            name='picture',
        ),
        migrations.AddField(
            model_name='citizendocument',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='citizens/documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Document'),
        ),
    ]
