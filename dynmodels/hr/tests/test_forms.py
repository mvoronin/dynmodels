# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from hr.forms import get_form_class
from hr.models import get_model_class


class DepartmentFormTest(TestCase):

    def setUp(self):
        cls_dict = {
            "module": "hr",
            "name": "Department",
            "fields": [{"name": "name", "title": "Название", "type": "char", "length": 100}]
        }
        self.ModelClass = get_model_class(cls_dict)
        self.FormClass = get_form_class(cls_dict, self.ModelClass)

    def test_valid_form(self):
        data = {'name': 'Support'}
        form = self.FormClass(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'name': None}
        form = self.FormClass(data=data)
        self.assertFalse(form.is_valid())
