# Generated by Django 4.1.1 on 2022-10-20 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='admin', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni_admin', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('date_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('cellphone_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id_book', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('literary_gender', models.CharField(choices=[('1', 'Universal literature'), ('2', 'General'), ('3', 'Terror and suspense'), ('4', 'Historical'), ('5', 'Romance'), ('6', 'Science fiction and Fantasy')], max_length=200)),
                ('number_pages', models.IntegerField()),
                ('editorial', models.CharField(max_length=200)),
                ('issn', models.IntegerField()),
                ('idiom', models.CharField(max_length=200)),
                ('publication_date', models.DateTimeField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('digital', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BranchOffice',
            fields=[
                ('id_branch_office', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('admin', models.ManyToManyField(to='store.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='customer', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('date_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('cellphone_number', models.IntegerField(null=True)),
                ('literary_prefer', models.CharField(blank=True, choices=[('1', 'Universal literature'), ('2', 'General'), ('3', 'Terror and suspense'), ('4', 'Historical'), ('5', 'Romance'), ('6', 'Science fiction and Fantasy')], default='1', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.BigAutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('final_price', models.IntegerField(default=0)),
                ('complete', models.BooleanField(default=False)),
                ('dni_customer1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id_shipping', models.BigAutoField(primary_key=True, serialize=False)),
                ('state_shipping', models.CharField(choices=[('1', 'PREPARING'), ('2', 'SENT'), ('3', 'DELIVERED')], max_length=200)),
                ('date_shipping', models.DateField()),
                ('address_shipping', models.CharField(max_length=200)),
                ('order_number_shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id_schedule', models.BigAutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=200)),
                ('opening_hour', models.TimeField()),
                ('closing_hour', models.TimeField()),
                ('id_branch_office2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.branchoffice')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id_return_order', models.BigAutoField(primary_key=True, serialize=False)),
                ('cause', models.CharField(choices=[('1', 'Product in poor shape'), ('2', 'It did not meet my expectations'), ('3', 'The order arrived in a time superior to the stipulated", "The order arrived in a time superior to the stipulated')], max_length=200)),
                ('description', models.TextField(max_length=400)),
                ('order_number_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('branch_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.branchoffice')),
            ],
        ),
        migrations.CreateModel(
            name='PickUpStore',
            fields=[
                ('id_pickup_store', models.BigAutoField(primary_key=True, serialize=False)),
                ('state_shipping', models.CharField(choices=[('1', 'EN TIENDA'), ('2', 'RECOGIDO')], max_length=200)),
                ('branch_office_pickup', models.CharField(max_length=200)),
                ('order_number_pickup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id_details', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('book_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id_copy', models.BigAutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=10)),
                ('id_book_copy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('id_branch_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.branchoffice')),
                ('id_quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.quantity')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id_booking', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('booking_hour', models.TimeField(auto_now=True)),
                ('dni_customer2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('reserved_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
            ],
        ),
    ]
