# Generated by Django 3.1 on 2022-02-03 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oursite', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_date',)},
        ),
    ]