# Generated by Django 5.0.3 on 2024-03-09 15:51

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices_analyzer', '0021_remove_userrouts_depot_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productionplace',
            options={'get_latest_by': 'modified'},
        ),
        migrations.CreateModel(
            name='UserRouts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='prices_analyzer.depot')),
                ('production_place', models.ManyToManyField(to='prices_analyzer.productionplace')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
