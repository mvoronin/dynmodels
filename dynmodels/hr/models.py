# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from django.core.urlresolvers import reverse
from django.db import models

cls_dict_list = [
    {
        'module': 'hr',
        'name': 'Department',
        'fields': {
            'name': 'char(100)'
        }
    },
    {
        'module': 'hr',
        'name': 'Room',
        'fields': {
            'number': 'char(4)'
        }
    },
    {
        'module': 'hr',
        'name': 'Employee',
        'fields': {
            'name': 'char(100)',
            'email': 'email',
            'salary': 'decimal(8,2)',
            'begin_date': 'date',
            'department': 'fkey(hr.Department)',
            'room': 'fkey(hr.Room)'
        }
    },
    {
        'module': 'hr',
        'name': 'Computer',
        'fields': {
            'department': 'fkey(hr.Department)',
            'room': 'fkey(hr.Room)'
        }
    }
]

corresp_dict = {
    'fkey': models.ForeignKey,
    'int': models.IntegerField,
    'float': models.FloatField,
    'decimal': models.DecimalField,
    'char': models.CharField,
    'date': models.DateField,
    'datetime': models.DateTimeField,
    'email': models.EmailField
}


class ModelURLMixin(object):
    def get_list_url(self):
        return reverse('%(model)s-list' % {'model': self.__class__.__name__.lower()})

    def get_create_url(self):
        return reverse('%(model)s-create' % {'model': self.__class__.__name__.lower()})

    @models.permalink
    def get_update_url(self):
        return '%(model)s-update' % {'model': self.__class__.__name__.lower()}, (), {'pk': self.pk}

    @models.permalink
    def get_delete_url(self):
        return '%(model)s-delete' % {'model': self.__class__.__name__.lower()}, (), {'pk': self.pk}


class ModelBaseMixin(object):
    def __str__(self):
        return str(self.__class__.__name__)

    def __unicode__(self):
        return unicode(self.__class__.__name__)

    def name(self):
        return self.__unicode__()

    def lname(self):
        return self.__unicode__().lower()


def get_model_field(attr_type):
    args = []
    kwargs = dict()

    match = re.search(r'(char)\s*\((\d+)\)', attr_type, re.I)
    if match:
        attr_type = match.group(1)
        kwargs.update({'max_length': int(match.group(2))})

    match = re.search(r'(decimal)\s*\((\d+),(\d+)\)', attr_type, re.I)
    if match:
        attr_type = match.group(1)
        kwargs.update({'max_digits': int(match.group(2)),
                       'decimal_places': int(match.group(3))})

    match = re.search(r'(fkey)\s*\((\w+\.\w+)\)', attr_type, re.I)
    if match:
        attr_type = match.group(1)
        args += [match.group(2)]

    try:
        field = corresp_dict[attr_type](*args, **kwargs)
    except KeyError:
        return None

    return field


def get_model_class(class_dict):
    ClassObj = None

    try:
        ClassObj = models.get_model(class_dict['module'], class_dict['name'].capitalize())
    except LookupError:
        pass

    if ClassObj is None:
        attr_dict = {'__module__': '%s.%s' % (class_dict['module'], class_dict['name'])}
        for attr_name, attr_type in class_dict['fields'].iteritems():
            attr_dict.update({attr_name: get_model_field(attr_type)})

        ClassObj = type(
            str(class_dict['name']),
            (ModelBaseMixin, models.Model, ModelURLMixin),
            attr_dict
        )

    return ClassObj
