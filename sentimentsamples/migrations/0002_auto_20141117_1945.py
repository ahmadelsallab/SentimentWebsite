# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentimentsamples', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='sentiment',
            field=models.CharField(choices=[(0, 'Positive'), (1, 'Negative'), (2, 'Neutral')], max_length=10, default=2),
            preserve_default=True,
        ),
    ]
