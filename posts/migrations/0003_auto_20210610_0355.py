# Generated by Django 3.1.6 on 2021-06-10 03:55

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210415_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
