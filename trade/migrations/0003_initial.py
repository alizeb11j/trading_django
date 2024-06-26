# Generated by Django 5.0.2 on 2024-02-26 20:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trade', '0002_delete_kraken'),
    ]

    operations = [
        migrations.CreateModel(
            name='AltCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.FloatField()),
                ('alt_time_update', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Kraken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BTC', models.FloatField()),
                ('Price', models.FloatField()),
                ('kra_time_update', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
