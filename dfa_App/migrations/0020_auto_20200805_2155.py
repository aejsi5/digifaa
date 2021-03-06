# Generated by Django 3.0.1 on 2020-08-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0019_auto_20200805_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_EXTERNAL_ID_FROM',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Flottennummer von'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_EXTERNAL_ID_FROM_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_EXTERNAL_ID_TO',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Flottennummer bis'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_EXTERNAL_ID_TO_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO',
            field=models.DateField(blank=True, null=True, verbose_name='Erstzulassungsdatum bis'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MAKE_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_MODEL_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_SERIES_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_TYPE_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_USER_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_VIN_FROM_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='Constraint_Vehicle_VIN_TO_CHOICES',
            field=models.SmallIntegerField(choices=[(0, 'gleich'), (1, 'nicht gleich'), (2, 'enthält'), (3, 'enthält nicht'), (4, 'beginnt mit'), (5, 'beginnt nicht mit'), (6, 'endet mit'), (7, 'endet nicht mit')], default=0, verbose_name='Beschränkung'),
        ),
        migrations.AlterField(
            model_name='constraint',
            name='Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM',
            field=models.DateField(blank=True, null=True, verbose_name='Erstzulassungsdatum von'),
        ),
    ]
