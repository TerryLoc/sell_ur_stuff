# Generated by Django 5.1.6 on 2025-03-17 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_sale_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='image',
            new_name='main_image',
        ),
    ]
