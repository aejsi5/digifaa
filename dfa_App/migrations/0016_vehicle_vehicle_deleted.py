# Generated by Django 3.0.1 on 2020-08-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0015_vehicel_recall_vr_last_update_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='Vehicle_DELETED',
            field=models.BooleanField(default=False, verbose_name='Gelöscht'),
        ),
    ]
