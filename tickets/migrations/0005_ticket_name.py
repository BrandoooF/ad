# Generated by Django 2.0.9 on 2019-04-25 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20190422_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default=True, max_length=60),
        ),
    ]