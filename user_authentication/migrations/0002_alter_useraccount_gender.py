# Generated by Django 5.0.2 on 2024-03-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(choices=[('MALE', 'M'), ('FEMALE', 'F'), ('OTHERS', 'O')], max_length=10),
        ),
    ]