# Generated by Django 3.2.7 on 2021-09-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20210904_1433'),
    ]

    operations = [
        migrations.DeleteModel(
            name='nsiIkul',
        ),
        migrations.DeleteModel(
            name='nsiOkogu',
        ),
        migrations.DeleteModel(
            name='nsiOkpd',
        ),
        migrations.DeleteModel(
            name='nsiOkv',
        ),
        migrations.DeleteModel(
            name='nsiPPO',
        ),
        migrations.RemoveField(
            model_name='organizationokved',
            name='okved',
        ),
        migrations.RemoveField(
            model_name='organizationokved',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='nsiokei',
            name='group',
        ),
        migrations.RemoveField(
            model_name='nsiokei',
            name='section',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='okato',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='okfs',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='okopf',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='okpo',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='oktmo',
        ),
        migrations.AlterField(
            model_name='nsiokpd2',
            name='code',
            field=models.CharField(max_length=20, verbose_name='Код ОКПД2'),
        ),
        migrations.DeleteModel(
            name='nsiOkato',
        ),
        migrations.DeleteModel(
            name='nsiOkeiGroup',
        ),
        migrations.DeleteModel(
            name='nsiOkeiSection',
        ),
        migrations.DeleteModel(
            name='nsiOkfs',
        ),
        migrations.DeleteModel(
            name='nsiOkopf',
        ),
        migrations.DeleteModel(
            name='nsiOkpo',
        ),
        migrations.DeleteModel(
            name='nsiOktmo',
        ),
        migrations.DeleteModel(
            name='nsiOkved',
        ),
        migrations.DeleteModel(
            name='OrganizationOkved',
        ),
    ]