# Generated by Django 5.0.7 on 2024-07-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=models.TextField(default=None, max_length=1024),
        ),
        migrations.AlterField(
            model_name='posts',
            name='picture',
            field=models.TextField(default=None, null=True),
        ),
    ]
