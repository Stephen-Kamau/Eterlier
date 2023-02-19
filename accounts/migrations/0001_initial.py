# Generated by Django 4.0.5 on 2023-02-05 08:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Hotel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=500, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'eaterlier_Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_to_be_delivered', models.BooleanField(default=True, max_length=100)),
                ('comments', models.CharField(blank=True, max_length=500)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customerOrders', to='accounts.customer')),
            ],
            options={
                'db_table': 'eaterlier_Orders',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=500, primary_key=True, serialize=False, unique=True)),
                ('is_manager', models.BooleanField(default=False, verbose_name='Manager status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff status')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Customer status')),
                ('user_name', models.CharField(blank=True, max_length=30, verbose_name='user_name')),
                ('email', models.EmailField(max_length=90, unique=True, verbose_name='Email')),
                ('user_phone', models.CharField(max_length=15, null=True, unique=True, verbose_name='Telephone number')),
                ('user_gender', models.CharField(max_length=15, verbose_name='Gender')),
                ('user_password', models.TextField(max_length=200, verbose_name='Password')),
                ('user_address', models.TextField(max_length=200, verbose_name='Address')),
                ('user_state', models.TextField(max_length=200, verbose_name='State')),
                ('user_country', models.TextField(max_length=200, verbose_name='Country')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'eaterlier_USERs',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('jobtitle', models.CharField(max_length=200, verbose_name='Title')),
                ('work_shift', models.CharField(max_length=200, verbose_name='shift')),
                ('branch_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffBranch', to='Hotel.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='accounts.user')),
            ],
            options={
                'db_table': 'eaterlier_Staffs',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_red', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paymentOrder', to='accounts.order')),
            ],
            options={
                'db_table': 'eaterlier_orderPayments',
            },
        ),
        migrations.CreateModel(
            name='otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.TextField(max_length=20, verbose_name='OTP CODE')),
                ('validated', models.BooleanField(default=False)),
                ('password_reset_code', models.TextField(default='', max_length=20, verbose_name='Reset Code')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'db_table': 'eaterlier_OTP_Code',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('order_product_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RefOrdered', to='accounts.order')),
                ('product_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productordered', to='Hotel.foodproduct')),
            ],
            options={
                'db_table': 'eaterlier_ProductOrders',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('branch_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branchManager', to='Hotel.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='accounts.user')),
            ],
            options={
                'db_table': 'eaterlier_Managers',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='accounts.user'),
        ),
    ]
