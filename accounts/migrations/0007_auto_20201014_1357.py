# Generated by Django 3.0.5 on 2020-10-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201014_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='sec_num',
            field=models.IntegerField(default=7716620813),
        ),
    ]
