# Generated by Django 5.1.6 on 2025-03-22 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newslettersubscriber',
            options={'ordering': ('-subscribed_at',), 'verbose_name': 'Newsletter Subscriber', 'verbose_name_plural': 'Newsletter Subscribers'},
        ),
    ]
