# Generated by Django 3.2.7 on 2021-09-04 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_query_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personcontacts',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personcontacts',
            name='type',
        ),
        migrations.RemoveField(
            model_name='organizationcontacts',
            name='person',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='PersonContacts',
        ),
    ]
