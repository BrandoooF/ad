# Generated by Django 2.0.9 on 2019-05-13 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190513_2002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='long',
            new_name='lng',
        ),
    ]