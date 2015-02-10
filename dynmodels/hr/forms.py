# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.forms import ModelForm
from django.forms.models import ModelFormMetaclass


def get_form_class(class_dict, ClassObj):
    MetaClass = type(str("Meta"), (ModelFormMetaclass, ), {
        'model': ClassObj,
        'fields': [x['name'] for x in class_dict['fields']]
    })

    FormClass = type(
        str(class_dict['name'].capitalize() + 'ModelForm'),
        (ModelForm, ),
        {
            'Meta': MetaClass
        }
    )
    return FormClass
