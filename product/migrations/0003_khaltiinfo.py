# Generated by Django 5.0.2 on 2024-03-26 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KhaltiInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pixd', models.CharField(max_length=250)),
                ('transaction_id', models.CharField(max_length=250)),
                ('tidx', models.CharField(max_length=250)),
                ('amount', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('mobile', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=250)),
                ('purchase_order_id', models.CharField(max_length=250)),
                ('purchase_order_name', models.CharField(max_length=250)),
            ],
        ),
    ]
