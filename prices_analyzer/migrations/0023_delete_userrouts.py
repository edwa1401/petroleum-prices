# Generated by Django 5.0.3 on 2024-03-13 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prices_analyzer', '0022_alter_productionplace_options_userrouts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserRouts',
        ),
    ]
