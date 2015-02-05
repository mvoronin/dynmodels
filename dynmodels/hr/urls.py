# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import *
from hr.models import cls_dict_list, get_model_class
from hr.views import get_list_view_class, get_detail_view_class, \
    get_create_view_class, get_update_view_class, get_delete_view_class


urlpatterns = patterns('hr.views',
    url(r'^$', 'index', name='index'),
)

for cls_dict in cls_dict_list:
    model_cls = get_model_class(cls_dict)
    list_view_cls = get_list_view_class(cls_dict, model_cls)
    detail_view_cls = get_detail_view_class(cls_dict, model_cls)
    create_view_cls = get_create_view_class(cls_dict, model_cls)
    update_view_cls = get_update_view_class(cls_dict, model_cls)
    delete_view_cls = get_delete_view_class(cls_dict, model_cls)

    urlpatterns += patterns('',
        url(r'^%(model_label)s/$' % {'model_label': cls_dict['name'].lower()}, list_view_cls.as_view(),
            name=cls_dict['name'].lower() + '-list'),
        url(r'^%(model_label)s/(?P<pk>\d+)$' % {'model_label': cls_dict['name'].lower()}, detail_view_cls.as_view(),
            name=cls_dict['name'].lower() + '-detail'),
        url(r'^%(model_label)s/create$' % {'model_label': cls_dict['name'].lower()}, create_view_cls.as_view(),
            name=cls_dict['name'].lower() + '-create'),
        url(r'^%(model_label)s/(?P<pk>\d+)/update$' % {'model_label': cls_dict['name'].lower()}, update_view_cls.as_view(),
            name=cls_dict['name'].lower() + '-update'),
        url(r'^%(model_label)s/(?P<pk>\d+)/delete$' % {'model_label': cls_dict['name'].lower()}, delete_view_cls.as_view(),
            name=cls_dict['name'].lower() + '-delete'),
    )
