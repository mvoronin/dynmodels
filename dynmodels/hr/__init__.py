# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.conf import settings

cls_dict_list = []
default_app_config = 'hr.apps.HRConfig'

filepath = settings.APPS_INPUT_FILES['hr']
json_data = open(filepath, 'r')
cls_dict_list = json.load(json_data)
json_data.close()
