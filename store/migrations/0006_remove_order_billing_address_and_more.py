# Generated by Django 5.1.2 on 2024-11-13 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_billingaddress_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='total_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='Temporary Address', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='COD', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='BillingAddress',
        ),
    ]
