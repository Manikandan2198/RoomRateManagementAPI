# Generated by Django 5.0.6 on 2024-07-06 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='roomrate',
            name='room_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
