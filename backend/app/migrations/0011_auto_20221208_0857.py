# Generated by Django 3.2.16 on 2022-12-08 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_nome_wilaya_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Commune',
        ),
        migrations.DeleteModel(
            name='Wilaya',
        ),
    ]
