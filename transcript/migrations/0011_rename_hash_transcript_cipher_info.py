# Generated by Django 4.0.3 on 2022-06-03 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0010_remove_transcript_info_encrypt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transcript',
            old_name='hash',
            new_name='cipher_info',
        ),
    ]
