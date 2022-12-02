# Generated by Django 4.1.1 on 2022-11-13 20:59

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('store', '0033_alter_booking_booking_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='region', chained_model_field='region', null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.city'),
        ),
        migrations.AddField(
            model_name='shipping',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.country'),
        ),
        migrations.AddField(
            model_name='shipping',
            name='region',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.region'),
        ),
    ]
