# Generated by Django 4.2.6 on 2023-10-30 19:37

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Petroleum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('product_key', models.CharField(max_length=4)),
                ('base', models.CharField(max_length=3)),
                ('base_name', models.CharField(max_length=1000)),
                ('volume', models.SmallIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('metric', models.CharField(choices=[('Килограмм', 'Kg'), ('Метрическая тонна', 'Tn')], max_length=20)),
                ('day', models.DateField()),
                ('sort', models.CharField(choices=[('AI100', 'Ai100'), ('AI98', 'Ai98'), ('AI95', 'Ai95'), ('AI92', 'Ai92'), ('DTL', 'Dtl'), ('DTD', 'Dtd'), ('DTZ', 'Dtz'), ('Other products', 'Other Products')], max_length=15)),
                ('density', models.DecimalField(decimal_places=2, max_digits=4)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
