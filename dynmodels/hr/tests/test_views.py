# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test import Client


class RavenTestCase(TestCase):
    def assertStatusCodeEqual(self, request, expected_status_code, msg_prefix='', msg_postfix=''):
        """
        Fail if the returned status code and expected status code are unequal.
        Args:
            request (HttpRequest): The request object.
            expected_status_code (int): The expected status code.
            msg_prefix (str, optional): The message prefix.
            msg_postfix (str, optional): The message postfix.
        """

        assertion_func = self._getAssertEqualityFunc(request.status_code, expected_status_code)
        assertion_func(request.status_code, expected_status_code,
                       msg='%s returned status [%s] != expected status [%s] %s' %
                           (msg_prefix, request.status_code, expected_status_code, msg_postfix))


class IndexViewTest(RavenTestCase):
    def setUp(self):
        self.client = Client()

    def test_list_view(self):
        page_url = '/dynmodels/'

        expected_status_code = 200
        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code)


class DepartmentViewsTest(RavenTestCase):
    fixtures = ['test/department.json']
    base_url = '/dynmodels/department/'
    models_urls = dict()
    pk = 1

    def setUp(self):
        self.models_urls.update({
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })

    def test_create_view_get(self):
        page_url = self.models_urls['create']
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_get_ajax(self):
        page_url = self.models_urls['create']
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {'name': 'Sales'}

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post_ajax_valid(self):
        page_url = self.models_urls['create']
        expected_status_code = 200
        data = {'name': 'Sales'}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_create_view_post_ajax_invalid(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {'name': ''}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {
            'result': 'invalid',
            'error': {
                'name': ['This field is required.']
            }
        })

    def test_update_view_get(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_get_ajax(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {'name': 'Sales'}

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post_ajax_valid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200
        data = {'name': 'Sales'}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_update_view_post_ajax_invalid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {'name': ''}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {
            'result': 'invalid',
            'error': {
                'name': ['This field is required.']
            }
        })

    def test_delete_view_get(self):
        page_url = self.models_urls['delete'] % self.pk
        expected_status_code = 405

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_delete_view_get_ajax(self):
        page_url = self.models_urls['delete'] % self.pk
        expected_status_code = 405

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_delete_view_post(self):
        page_url = self.models_urls['delete'] % self.pk
        expected_status_code = 400

        response = self.client.post(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_delete_view_post_ajax_valid(self):
        page_url = self.models_urls['delete'] % self.pk
        expected_status_code = 200

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_delete_view_post_ajax_invalid(self):
        page_url = self.models_urls['delete'] % 999
        expected_status_code = 404

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)


class RoomViewsTest(RavenTestCase):
    fixtures = ['test/department.json', 'test/room.json']
    base_url = '/dynmodels/room/'
    models_urls = dict()
    pk = 1

    def setUp(self):
        self.models_urls.update({
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })

    def test_create_view_get(self):
        page_url = self.models_urls['create']
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_get_ajax(self):
        page_url = self.models_urls['create']
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post_ajax_valid(self):
        page_url = self.models_urls['create']
        expected_status_code = 200
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_create_view_post_ajax_invalid(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {
            'number': '1',
            'department': '',
            'spots': '10'
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'invalid', 'error': {'department': ['This field is required.']}})

    def test_update_view_get(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_get_ajax(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post_ajax_valid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200
        data = {
            'number': '1',
            'department': '1',
            'spots': '10'
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_update_view_post_ajax_invalid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {
            'number': '1',
            'department': '',
            'spots': '10'
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {
            'result': 'invalid',
            'error': {
                'department': ['This field is required.']
            }
        })


class EmployeeViewsTest(RavenTestCase):
    fixtures = ['test/department.json', 'test/room.json', 'test/employee.json']
    base_url = '/dynmodels/employee/'
    models_urls = dict()
    pk = 1

    def setUp(self):
        self.model_name = 'employee'
        self.models_urls.update({
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })

    def test_create_view_get(self):
        page_url = self.models_urls['create']
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_get_ajax(self):
        page_url = self.models_urls['create']
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {
            'name': 'John Smith',
            'email': 'smith@mail.com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_create_view_post_ajax_valid(self):
        page_url = self.models_urls['create']
        expected_status_code = 200
        data = {
            'name': 'John Smith',
            'email': 'smith@mail.com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_create_view_post_ajax_invalid(self):
        page_url = self.models_urls['create']
        expected_status_code = 400
        data = {
            'name': 'John Smith',
            'email': 'smith@com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {
            'result': 'invalid',
            'error': {
                'email': ['Enter a valid email address.']
            }
        })

    def test_update_view_get(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_get_ajax(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {
            'name': 'John Smith',
            'email': 'smith@mail.com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_update_view_post_ajax_valid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 200
        data = {
            'name': 'John Smith',
            'email': 'smith@mail.com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

    def test_update_view_post_ajax_invalid(self):
        page_url = self.models_urls['update'] % self.pk
        expected_status_code = 400
        data = {
            'name': 'John Smith',
            'email': 'smith@com',
            'salary': 52500.00,
            'begin_date': '2015-01-01',
            'department': 1
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {
            'result': 'invalid',
            'error': {
                'email': ['Enter a valid email address.']
            }
        })
