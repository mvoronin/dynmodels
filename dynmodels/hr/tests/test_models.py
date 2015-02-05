# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.test import TestCase
from hr.models import get_model_field


class ModelTest(TestCase):

    def test_field_type_detection(self):
        field_str_list = {
            'int': (models.IntegerField, None),
            'float': (models.FloatField, None),
            'decimal(8,2)': (models.DecimalField,
                             {'max_digits': 8, 'decimal_places': 2}),
            'char(100)': (models.CharField,
                          {'max_length': 100}),
            'date': (models.DateField, None),
            'datetime': (models.DateTimeField, None),
            'email': (models.EmailField, None),
            'fkey': (models.ForeignKey, {'to': 'hr.Department'})
        }

        for str_type, tuple_cls in field_str_list.iteritems():
            cls, attrs = tuple_cls
            field = get_model_field(str_type)
            self.assertEqual(cls, field.__class__,
                             msg='For alias "%s" should be used class %s, not %s!' %
                                 (str_type, cls.__name__, field.__class__.__name__))
            if attrs is None:
                continue

            for attr, value in attrs.iteritems():
                self.assertTrue(hasattr(field, attr),
                                msg='Attribute "%s" is not exists in field "%s"!' %
                                    (attr, field.__class__.__name__))
                self.assertEqual(getattr(field, attr), value,
                                 msg='Value of attribute "%s" (class "%s") should be equal %s, not %s' %
                                     (attr, cls.__name__, value, getattr(field, attr)))
