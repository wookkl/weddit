# Generated by Django 2.2.5 on 2021-03-01 03:48

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
