# Generated by Django 4.2.1 on 2023-07-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0009_alter_review_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='storyline',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
