# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.test import TestCase
from hr.models import get_field


class ModelTest(TestCase):

    def test_field_type_detection(self):
        field_corresp_dict = {
            'int': models.IntegerField,
            'float': models.FloatField,
            'decimal': models.DecimalField,
            'char': models.CharField,
            'date': models.DateField,
            'datetime': models.DateTimeField,
            'email': models.EmailField,
            'fkey': models.ForeignKey
        }
        test_field_dsc_list = [
            {"name": "number", "type": "char", "length": 5},
            {"name": "department", "type": "fkey", "ref": "hr.Department"},
            {"name": "spots", "type": "int"}
        ]

        for fdict in test_field_dsc_list:
            field_name, field_cls = get_field(fdict)
            expect_cls = field_corresp_dict[fdict['type']]
            self.assertEqual(expect_cls, field_cls.__class__,
                             msg='For alias "%s" should be used class %s, not %s!' %
                                 (fdict['type'], expect_cls.__name__, field_cls.__class__.__name__))

            # for attr, value in attrs.iteritems():
            #     self.assertTrue(hasattr(field, attr),
            #                     msg='Attribute "%s" is not exists in field "%s"!' %
            #                         (attr, field.__class__.__name__))
            #     self.assertEqual(getattr(field, attr), value,
            #                      msg='Value of attribute "%s" (class "%s") should be equal %s, not %s' %
            #                          (attr, cls.__name__, value, getattr(field, attr)))
