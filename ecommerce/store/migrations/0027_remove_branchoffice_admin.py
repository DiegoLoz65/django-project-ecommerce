# Generated by Django 4.1.1 on 2022-11-09 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_branchoffice_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchoffice',
            name='admin',
        ),
    ]