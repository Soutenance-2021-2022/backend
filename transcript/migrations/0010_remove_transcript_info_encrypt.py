# Generated by Django 4.0.3 on 2022-05-28 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0009_transcript_decision_transcript_hash_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='info_encrypt',
        ),
    ]