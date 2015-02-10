# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.db import models


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

    def get_update_url(self):
        return reverse('%(model)s-update' % {'model': self.__class__.__name__.lower()}, kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('%(model)s-delete' % {'model': self.__class__.__name__.lower()}, kwargs={'pk': self.pk})


class ModelBaseMixin(object):
    def __str__(self):
        return str(self.__class__.__name__)

    def __unicode__(self):
        return unicode(self.__class__.__name__)

    def name(self):
        return self.__unicode__()

    def lname(self):
        return self.__unicode__().lower()


def get_field(field_dsc):
    args = []
    kwargs = dict()

    ft = field_dsc['type']
    if ft == 'fkey':
        args.insert(0, field_dsc['ref'])
    elif ft == 'decimal':
        kwargs.update({'max_digits': field_dsc['digits'], 'decimal_places': field_dsc['decimal_places']})
    elif ft == 'char':
        kwargs.update({'max_length': field_dsc['length']})

    if 'title' in field_dsc:
        kwargs.update({'verbose_name': field_dsc['title']})

    if 'null' in field_dsc:
        kwargs.update({'null': field_dsc['null']})

    try:
        field = corresp_dict[field_dsc['type']](*args, **kwargs)
    except KeyError:
        return None

    return field_dsc['name'], field


def get_model_class(class_dict):
    ClassObj = None

    try:
        ClassObj = models.get_model(class_dict['module'], class_dict['name'].capitalize())
    except LookupError:
        pass

    if ClassObj is None:
        attr_dict = {'__module__': '%s.%s' % (class_dict['module'], class_dict['name'])}
        for field_dsc in class_dict['fields']:
            field_name, field_obj = get_field(field_dsc)
            attr_dict.update({field_name: field_obj})

        ClassObj = type(
            str(class_dict['name']),
            (ModelBaseMixin, ModelURLMixin, models.Model),
            attr_dict
        )

    return ClassObj
