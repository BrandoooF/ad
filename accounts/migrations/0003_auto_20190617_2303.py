# Generated by Django 2.0.9 on 2019-06-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receives_emails',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='receives_emails_from_organizers',
            field=models.BooleanField(default=True),
        ),
    ]
