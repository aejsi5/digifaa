# Generated by Django 3.0.1 on 2020-12-05 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfa_App', '0034_auto_20200926_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constraint',
            name='Constraint_PATH',
            field=models.FilePathField(blank=True, default=None, null=True, path='/home/felixw/digifaa/dfa_App/media/constraints'),
        ),
    ]
