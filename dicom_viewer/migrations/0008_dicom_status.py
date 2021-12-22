# Generated by Django 3.2.9 on 2021-12-22 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicom_viewer', '0007_dicom_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicom',
            name='status',
            field=models.CharField(choices=[('none', 'None'), ('uploaded', 'Uploaded'), ('broken', 'Broken')], default='none', max_length=20),
        ),
    ]
