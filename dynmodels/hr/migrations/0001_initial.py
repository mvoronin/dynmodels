# -*- coding: utf-8 -*-
from django.db import models, migrations
import hr.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
            },
            bases=(hr.models.ModelBaseMixin, models.Model, hr.models.ModelURLMixin),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('email', models.EmailField(max_length=75)),
                ('salary', models.DecimalField(max_digits=8, decimal_places=2)),
                ('begin_date', models.DateField()),
                ('department', models.ForeignKey(to='hr.Department')),
            ],
            options={
            },
            bases=(hr.models.ModelBaseMixin, models.Model, hr.models.ModelURLMixin),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=5, verbose_name='\u041d\u043e\u043c\u0435\u0440')),
                ('spots', models.IntegerField(verbose_name='\u0412\u043c\u0435\u0441\u0442\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c')),
                ('department', models.ForeignKey(verbose_name='\u041e\u0442\u0434\u0435\u043b', to='hr.Department')),
            ],
            options={
            },
            bases=(hr.models.ModelBaseMixin, models.Model, hr.models.ModelURLMixin),
        ),
    ]
