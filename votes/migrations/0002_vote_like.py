# Generated by Django 2.2.5 on 2021-04-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='like',
            field=models.BooleanField(default=True),
        ),
    ]
