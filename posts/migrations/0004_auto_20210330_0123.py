# Generated by Django 2.2.5 on 2021-03-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210324_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/posts/'),
        ),
    ]
