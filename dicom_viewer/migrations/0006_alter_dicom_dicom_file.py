# Generated by Django 3.2.9 on 2021-12-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicom_viewer', '0005_alter_dicom_dicom_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicom',
            name='dicom_file',
            field=models.FileField(upload_to='dicoms/'),
        ),
    ]
