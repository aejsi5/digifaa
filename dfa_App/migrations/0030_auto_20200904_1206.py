# Generated by Django 3.0.1 on 2020-09-04 10:06

import dfa_App.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0029_auto_20200904_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recall_doc',
            name='Document_PATH',
            field=models.FileField(max_length=500, upload_to=dfa_App.models.update_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Upload Pfad'),
        ),
    ]
