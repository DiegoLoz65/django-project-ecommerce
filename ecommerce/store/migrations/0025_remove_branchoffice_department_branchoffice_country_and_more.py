# Generated by Django 4.1.1 on 2022-11-08 22:00

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('store', '0024_alter_paymentmethod_cardholder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchoffice',
            name='department',
        ),
        migrations.AddField(
            model_name='branchoffice',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.country'),
        ),
        migrations.AddField(
            model_name='branchoffice',
            name='region',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.region'),
        ),
        migrations.AlterField(
            model_name='branchoffice',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='region', chained_model_field='region', null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.city'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
