# Generated by Django 4.1.1 on 2022-11-06 00:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_customer_cellphone_number_alter_customer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Please enter a valid name', regex='[a-zA-Z_.-]+$')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='surname',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Please enter a valid surname', regex='[a-zA-Z_.-]+$')]),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='number_card',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator(message='Please enter a valid number card.', regex='^(?:4\\d([\\- ])?\\d{6}\\1\\d{5}|(?:4\\d{3}|5[1-5]\\d{2}|6011)([\\- ])?\\d{4}\\2\\d{4}\\2\\d{4})$')]),
        ),
    ]
