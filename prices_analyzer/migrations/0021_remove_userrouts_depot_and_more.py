# Generated by Django 4.2.9 on 2024-03-04 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prices_analyzer', '0020_alter_userrouts_options_fullprices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrouts',
            name='depot',
        ),
        migrations.RemoveField(
            model_name='userrouts',
            name='production_place',
        ),
        migrations.AlterModelOptions(
            name='productionplace',
            options={'get_latest_by': 'created', 'ordering': ['name']},
        ),
        migrations.DeleteModel(
            name='FullPrices',
        ),
        migrations.DeleteModel(
            name='UserRouts',
        ),
    ]
