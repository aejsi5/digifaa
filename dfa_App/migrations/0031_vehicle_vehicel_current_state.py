# Generated by Django 3.0.1 on 2020-09-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0030_auto_20200904_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='Vehicel_CURRENT_STATE',
            field=models.SmallIntegerField(choices=[(1, 'aktuell'), (0, 'nicht aktuell')], default=1, verbose_name='Aktueller Importstatus'),
        ),
    ]
