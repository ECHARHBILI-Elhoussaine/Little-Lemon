# Generated by Django 5.0.2 on 2024-02-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_price',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
