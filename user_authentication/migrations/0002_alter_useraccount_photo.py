# Generated by Django 5.0.2 on 2024-03-07 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/'),
        ),
    ]