# Generated by Django 5.2.2 on 2025-06-20 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_remove_review_reviewer_review_reviewer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='website.profile'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer_name',
            field=models.CharField(max_length=100),
        ),
    ]
