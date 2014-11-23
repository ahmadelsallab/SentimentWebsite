# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('sentiment', models.CharField(max_length=1, default=2, choices=[(0, 'Positive'), (1, 'Negative'), (2, 'Neutral')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
