# Generated by Django 4.1.1 on 2022-10-18 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_copy_id_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copy',
            name='id_quantity',
        ),
    ]