# Generated by Django 3.2.9 on 2022-01-05 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20220104_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorapplication',
            name='date_joined',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='spec',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='doctorapplication',
            name='spec',
            field=models.CharField(max_length=30),
        ),
    ]
