# Generated by Django 4.2.9 on 2024-01-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_densitymap'),
    ]

    operations = [
        migrations.AddField(
            model_name='petroleummap',
            name='petroleum_code',
            field=models.CharField(default=0, max_length=4),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PetroleumCode',
        ),
    ]
