# Generated by Django 5.1.6 on 2025-03-17 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_rename_image_sale_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
