# Generated by Django 2.2.5 on 2021-03-24 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20210301_0504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'default_related_name': 'subscriptions'},
        ),
    ]