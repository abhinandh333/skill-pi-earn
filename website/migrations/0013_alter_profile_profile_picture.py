# Generated by Django 5.2.2 on 2025-06-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_profile_created_at_profile_alternate_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/default.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
