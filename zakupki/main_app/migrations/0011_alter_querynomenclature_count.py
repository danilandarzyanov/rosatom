# Generated by Django 3.2.7 on 2021-09-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_rename_descritption_query_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querynomenclature',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
    ]
