# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.apps import AppConfig
# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured, AppRegistryNotReady
from hr.urls import patch_root_urlconf


class HRConfig(AppConfig):
    name = 'hr'
    verbose_name = "HR"

    def ready(self):

        # try:
        #     filepath = settings.APPS_INPUT_FILES['hr']
        # except KeyError:
        #     raise ImproperlyConfigured(
        #         "The app module %r can't find path to file with models description "
        #         "in the 'APPS_INPUT_FILES' variable." % self.name
        #     )
        #
        # try:
        #     json_data = open(filepath, 'r')
        # except IOError as e:
        #     raise AppRegistryNotReady(
        #         "The app module %r can't open file with models description. Path to file: \"%r\". I/O error(%s): %s" %
        #         (self.name, filepath, e.errno, e.strerror)
        #     )
        #
        # config.cls_dict_list = json.load(json_data)
        # json_data.close()

        patch_root_urlconf()

        super(HRConfig, self).ready()
