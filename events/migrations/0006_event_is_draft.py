# Generated by Django 2.0.9 on 2019-05-25 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
    ]
