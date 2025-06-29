# Generated by Django 5.2.2 on 2025-06-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_remove_profile_location_profile_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(default='unknow', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='district',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('owner', 'Shop/Enterprise Owner')], max_length=20),
        ),
    ]
