# Generated by Django 3.2.16 on 2022-12-08 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_delete_commune'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.wilaya')),
            ],
        ),
    ]
