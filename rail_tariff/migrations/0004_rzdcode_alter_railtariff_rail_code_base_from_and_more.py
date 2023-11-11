# Generated by Django 4.2.6 on 2023-11-10 14:35

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rail_tariff', '0003_remove_productionplace_basis_delete_depot_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RzdCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('code', models.SmallIntegerField()),
                ('station_name', models.CharField(blank=True, max_length=1000)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='railtariff',
            name='rail_code_base_from',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='rail_code_base_from', to='rail_tariff.rzdcode'),
        ),
        migrations.AlterField(
            model_name='railtariff',
            name='rail_code_base_to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='rail_code_base_to', to='rail_tariff.rzdcode'),
        ),
    ]
