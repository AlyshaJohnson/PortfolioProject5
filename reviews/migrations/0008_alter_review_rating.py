# Generated by Django 3.2.4 on 2023-02-27 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_remove_review_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(default=None, max_length=1),
        ),
    ]
