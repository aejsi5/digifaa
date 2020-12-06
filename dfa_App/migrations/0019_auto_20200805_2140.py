# Generated by Django 3.0.1 on 2020-08-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0018_workshop_workshop_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='constraint',
            name='Constraint_QUERY',
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM',
            field=models.DateField(blank=True, null=True, verbose_name='Erstzulassungsdatum bis'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MAKE',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Hersteller'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MILEAGE_FROM',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kilometerstand von'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MILEAGE_TO',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kilometerstand bis'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MODEL',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Modell'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_SERIES',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Baureihe'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_TYPE',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Typ'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_USER',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Fahrzeugnutzer'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_VIN_FROM',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='FIN von'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_VIN_TO',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='FIN bis'),
        ),
    ]
