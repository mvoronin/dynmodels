# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from hr.models import cls_dict_list, get_model_class


# {'hr.Employee': EmployeeAdminInline, 'hr.Computer': ComputerAdminInline}
dict_path_to_admin_model = dict()

# {'hr.Department': [EmployeeAdminInline, ComputerAdminInline], 'hr.Room': [EmployeeAdminInline, ComputerAdminInline]}
dict_model_inlines = dict()


def get_inline_admin_model_class(cls_dict):
    path_model = cls_dict['module']+'.'+cls_dict['name']

    if path_model in dict_path_to_admin_model:
        return dict_path_to_admin_model[path_model]
    else:
        ModelClass = get_model_class(cls_dict)
        AdminInlineModelClass = type(ModelClass.__name__+str('AdminInline'), (admin.TabularInline, ),
                                     {'__module__': cls_dict['module']+'.admin', 'model': ModelClass})
        dict_path_to_admin_model.update({path_model: AdminInlineModelClass})
        return AdminInlineModelClass


def create_inlines():
    for cls_dict in cls_dict_list:
        for field_name, field_type in cls_dict['fields'].iteritems():
            if field_type[:4] == 'fkey':
                path_fmodel = field_type[5:-1]
                path_model = cls_dict['module']+'.'+cls_dict['name']
                InlineAdminModelClass = get_inline_admin_model_class(cls_dict)
                if path_fmodel in dict_model_inlines:
                    inlines = dict_model_inlines[path_fmodel]
                else:
                    inlines = []
                    dict_model_inlines.update({path_fmodel: inlines})
                if InlineAdminModelClass not in inlines:
                    inlines += [InlineAdminModelClass]


create_inlines()

for cls_dict in cls_dict_list:
    path_model = cls_dict['module']+'.'+cls_dict['name']
    if path_model in dict_model_inlines:
        inlines = dict_model_inlines[path_model]
    else:
        inlines = []
    ModelClass = get_model_class(cls_dict)
    AdminModelClass = type(ModelClass.__name__+str('Admin'), (admin.ModelAdmin, ),
                           {'__module__': cls_dict['module']+'.admin', 'model': ModelClass, 'inlines': inlines})

    admin.site.register(ModelClass, AdminModelClass)
