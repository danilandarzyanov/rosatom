# Generated by Django 3.2.7 on 2021-09-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_organization_inn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='inn',
            field=models.CharField(max_length=20, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='kpp',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='КПП'),
        ),
    ]
