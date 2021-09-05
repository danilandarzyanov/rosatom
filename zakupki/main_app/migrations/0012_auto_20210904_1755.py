# Generated by Django 3.2.7 on 2021-09-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_querynomenclature_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomenclature',
            name='type',
            field=models.IntegerField(choices=[(0, 'Товар'), (1, 'Услуга')], default=0, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='querynomenclature',
            name='count',
            field=models.CharField(max_length=50, verbose_name='Количество'),
        ),
    ]