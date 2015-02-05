# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test import Client
from django.test.utils import override_settings

CACHES_DUMMY = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


@override_settings(CACHES=CACHES_DUMMY)
class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_list_view(self):
        page_url = '/dynmodels/'

        expected_status_code = 200
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, expected_status_code)
