# Generated by Django 3.2.16 on 2022-12-07 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20221207_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wilaya',
            old_name='nome',
            new_name='name',
        ),
    ]
