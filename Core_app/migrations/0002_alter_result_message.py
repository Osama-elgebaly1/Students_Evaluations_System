# Generated by Django 5.2 on 2025-04-29 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='message',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
