# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 05:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('birthday_wishes_app', '0018_auto_20160501_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='expires_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 5, 55, 24, 655230, tzinfo=utc)),
        ),
    ]