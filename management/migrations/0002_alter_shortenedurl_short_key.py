# Generated by Django 4.2.9 on 2024-01-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedurl',
            name='short_key',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
