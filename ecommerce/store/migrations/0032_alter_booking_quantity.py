# Generated by Django 4.1.1 on 2022-11-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_alter_book_literary_gender_alter_book_total_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
