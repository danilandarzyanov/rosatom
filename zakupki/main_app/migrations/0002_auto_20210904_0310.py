# Generated by Django 3.2.7 on 2021-09-03 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='inn',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='kpp',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='КПП'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='legalAddress',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Юридический адрес'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='ogrn',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='ОГРН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='okato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_nsiOkato', to='main_app.nsiokato', verbose_name='ОКАТО'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='okfs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_okfs', to='main_app.nsiokfs', verbose_name='ОКФС'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='okopf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_okopf', to='main_app.nsiokopf', verbose_name='ОКОПФ'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='okpo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_okpo', to='main_app.nsiokpo', verbose_name='ОКПО'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='oktmo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_oktmo', to='main_app.nsioktmo', verbose_name='ОКТМО'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='postalAddress',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Почтовый адрес'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата постановки на учет'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='timeZone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_timeZone', to='main_app.nsitimezone', verbose_name='Временная зона'),
        ),
    ]
