# Generated by Django 4.2.9 on 2024-01-26 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prices_analyzer', '0010_rename_price_prices_full_price'),
        ('rail_tariff', '0008_alter_railtariff_distance_alter_rzdcode_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RzdCode',
            new_name='RzdStation',
        ),
    ]