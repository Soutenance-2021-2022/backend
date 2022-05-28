# Generated by Django 4.0.3 on 2022-05-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0008_amphi_academic_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='decision',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='hash',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='info_encrypt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
