# Generated by Django 4.1.1 on 2022-11-02 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_rename_owner_paymentmethod_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='literary_gender',
            field=models.CharField(choices=[('Universal literature', 'Universal literature'), ('General', 'General'), ('Terror and suspense', 'Terror and suspense'), ('Historical', 'Historical'), ('Romance', 'Romance'), ('Science fiction and Fantasy', 'Science fiction and Fantasy')], max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='literary_prefer',
            field=models.CharField(blank=True, choices=[('Universal literature', 'Universal literature'), ('General', 'General'), ('Terror and suspense', 'Terror and suspense'), ('Historical', 'Historical'), ('Romance', 'Romance'), ('Science fiction and Fantasy', 'Science fiction and Fantasy')], default='1', max_length=200),
        ),
        migrations.AlterField(
            model_name='pickupstore',
            name='state_shipping',
            field=models.CharField(choices=[('EN TIENDA', 'EN TIENDA'), ('RECOGIDO', 'RECOGIDO')], max_length=200),
        ),
        migrations.AlterField(
            model_name='returnorder',
            name='cause',
            field=models.CharField(choices=[('Product in poor shape', 'Product in poor shape'), ('It did not meet my expectations', 'It did not meet my expectations'), ('The order arrived in a time superior to the stipulated", "The order arrived in a time superior to the stipulated', 'The order arrived in a time superior to the stipulated", "The order arrived in a time superior to the stipulated')], max_length=200),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='state_shipping',
            field=models.CharField(choices=[('PREPARING', 'PREPARING'), ('SENT', 'SENT'), ('DELIVERED', 'DELIVERED')], max_length=200),
        ),
    ]
