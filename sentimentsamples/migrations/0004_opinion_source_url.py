# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentimentsamples', '0003_auto_20141117_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='source_url',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=True,
        ),
    ]
