# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.loading import get_app, get_models
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from hr.mixins import RequestCheckMixin, AJAXListMixin, AJAXCreateView, AJAXUpdateView, AJAXDeleteView

logger = logging.getLogger(__name__)


def index(request):
    context = dict()
    app = get_app('hr')
    context.update({'models': get_models(app)})
    return render(request, "index.html", context)


def get_list_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'ListView'),
        (AJAXListMixin, ListView, ),
        {
            'model': ClassObj,
            'model_name': ClassObj.__name__,
            'allow_empty': True
        }
    )
    return ViewClass


def get_detail_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'DetailView'),
        (DetailView, ),
        {
            'model': ClassObj
        }
    )
    return ViewClass


def get_create_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'CreateView'),
        (AJAXCreateView, CreateView, ),
        {
            'model': ClassObj,
            'template_name': "form.html",
            'success_url': reverse_lazy('index'),
            'fields': [x['name'] for x in class_dict['fields']]
        }
    )
    return ViewClass


def get_update_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'UpdateView'),
        (AJAXUpdateView, UpdateView, ),
        {
            'model': ClassObj,
            'template_name': "form.html",
            'success_url': reverse_lazy('index'),
            'fields': [x['name'] for x in class_dict['fields']]
        }
    )
    return ViewClass


def get_delete_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'DeleteView'),
        (AJAXDeleteView, DeleteView, ),
        {
            'model': ClassObj,
            'success_url': reverse_lazy('index')
        }
    )
    return ViewClass
