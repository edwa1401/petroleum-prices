# Generated by Django 4.2.9 on 2024-01-26 11:06

from decimal import Decimal
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_remove_petroleummap_petroleum_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DensityMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('sort', models.CharField(choices=[('AI100', 'Ai100'), ('AI98', 'Ai98'), ('AI95', 'Ai95'), ('AI92', 'Ai92'), ('DTL', 'Dtl'), ('DTD', 'Dtd'), ('DTZ', 'Dtz'), ('Other products', 'Other Products')], max_length=20)),
                ('density', models.DecimalField(blank=True, choices=[(Decimal('0.75'), 'Ab'), (Decimal('0.83999999999999996891375531049561686813831329345703125'), 'Dt'), (Decimal('0'), 'Other Products')], decimal_places=2, max_digits=4)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
