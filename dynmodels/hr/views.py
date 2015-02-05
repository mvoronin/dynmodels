# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core import serializers
from django.db.models.loading import get_app, get_models
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class AJAXListMixin(object):
    def get_context_data(self, context_format='object', **kwargs):
        """
        Get the context for this view.
        """
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            if context_format == 'object':
                context = {
                    'paginator': paginator,
                    'page_obj': page,
                    'is_paginated': is_paginated,
                    'object_list': queryset
                }
            elif context_format == 'json':
                context = {
                    'paginator': {
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'page_range': paginator.page_range
                    },
                    'page_obj': {
                        'object_list': page.object_list.values(),
                        'number': page.number,
                        'has_next': page.has_next(),
                        'has_previous': page.has_previous(),
                        'has_other_pages': page.has_other_pages(),
                        'next_page_number': page.next_page_number(),
                        'previous_page_number': page.previous_page_number()
                    },
                    'is_paginated': is_paginated,
                    'object_list': json.loads(serializers.serialize("json", queryset))
                }
        else:
            if context_format == 'object':
                context = {
                    'paginator': None,
                    'page_obj': None,
                    'is_paginated': False,
                    'object_list': queryset
                }
            elif context_format == 'json':
                context = {
                    'paginator': None,
                    'page_obj': None,
                    'is_paginated': False,
                    'object_list': json.loads(serializers.serialize("json", queryset))
                }
        if context_format == 'object':
            if context_object_name is not None:
                context[context_object_name] = queryset
            context.update(kwargs)
            return super(AJAXListMixin, self).get_context_data(**context)
        else:
            return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if self.request.is_ajax():
            context = self.get_context_data(context_format='json')
            return self.render_to_json_response(context)
        else:
            context = self.get_context_data()
            return self.render_to_response(context)

    def render_to_json_response(self, context):
        return HttpResponse(json.dumps(context))


class AJAXCreateView(object):
    pass


class AJAXUpdateView(object):
    pass


class AJAXDeleteView(object):
    pass


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
            'allow_empty': True
        }
    )
    return ViewClass


def get_detail_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'DetailView'),
        (DetailView, ),
        {
            'model': ClassObj,
            'allow_empty': True
        }
    )
    return ViewClass


def get_create_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'CreateView'),
        (CreateView, ),
        {
            'model': ClassObj,
            'allow_empty': True
        }
    )
    return ViewClass


def get_update_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'UpdateView'),
        (UpdateView, ),
        {
            'model': ClassObj,
            'allow_empty': True
        }
    )
    return ViewClass


def get_delete_view_class(class_dict, ClassObj):
    ViewClass = type(
        str(class_dict['name'].capitalize() + 'DeleteView'),
        (DeleteView, ),
        {
            'model': ClassObj,
            'allow_empty': True
        }
    )
    return ViewClass
