# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
from django.apps import apps
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
    model_cls = None
    pk = 1

    def setUp(self):
        self.models_urls.update({
            'list': self.base_url,
            'detail': self.base_url + '%s',
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })
        self.model_cls = apps.get_model(app_label='hr', model_name='Department')

    def test_list_view_get(self):
        page_url = self.models_urls['list']
        expected_status_code = 400

        response = self.client.get(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_list_view_post(self):
        page_url = self.models_urls['list']
        expected_status_code = 405

        response = self.client.post(page_url)
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_list_view_get_ajax(self):
        page_url = self.models_urls['list']
        expected_status_code = 200

        response = self.client.get(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

    def test_list_view_post_ajax(self):
        page_url = self.models_urls['list']
        expected_status_code = 405

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)

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
        data = {'name': 'Space Science and Technology'}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

        self.assertTrue(self.model_cls.objects.filter(name='Space Science and Technology').exists())

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
        data = {'name': 'Space Science and Technology'}

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

        obj = self.model_cls.objects.get(pk=self.pk)
        self.assertEqual(obj.name, 'Space Science and Technology')

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

        self.assertFalse(self.model_cls.objects.filter(pk=self.pk).exists())

    def test_delete_view_post_ajax_invalid(self):
        page_url = self.models_urls['delete'] % 999
        expected_status_code = 404

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)


class RoomViewsTest(RavenTestCase):
    fixtures = ['test/department.json', 'test/room.json']
    base_url = '/dynmodels/room/'
    models_urls = dict()
    model_cls = None
    pk = 1

    def setUp(self):
        self.models_urls.update({
            'list': self.base_url,
            'detail': self.base_url + '%s',
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })
        self.model_cls = apps.get_model(app_label='hr', model_name='Room')

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

        self.assertTrue(self.model_cls.objects.filter(number='1', department=1, spots=10).exists())

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
            'number': '777',
            'department': '1',
            'spots': '999'
        }

        response = self.client.post(page_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
        self.assertJSONEqual(response.content, {'result': 'ok'})

        obj = self.model_cls.objects.get(pk=self.pk)
        self.assertEqual(obj.number, '777')
        self.assertEqual(obj.department_id, 1)
        self.assertEqual(obj.spots, 999)

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

        self.assertFalse(self.model_cls.objects.filter(pk=self.pk).exists())

    def test_delete_view_post_ajax_invalid(self):
        page_url = self.models_urls['delete'] % 999
        expected_status_code = 404

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)


class EmployeeViewsTest(RavenTestCase):
    fixtures = ['test/department.json', 'test/room.json', 'test/employee.json']
    base_url = '/dynmodels/employee/'
    models_urls = dict()
    model_cls = None
    pk = 1

    def setUp(self):
        self.model_name = 'employee'
        self.models_urls.update({
            'list': self.base_url,
            'detail': self.base_url + '%s',
            'create': self.base_url + 'create',
            'update': self.base_url + '%s/update',
            'delete': self.base_url + '%s/delete',
        })
        self.model_cls = apps.get_model(app_label='hr', model_name='Employee')

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

        self.assertTrue(self.model_cls.objects.filter(name='John Smith', email='smith@mail.com').exists())

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

        obj = self.model_cls.objects.get(pk=self.pk)
        self.assertEqual(obj.name, 'John Smith')
        self.assertEqual(obj.email, 'smith@mail.com')
        self.assertEqual(obj.salary, 52500.00)
        self.assertEqual(obj.begin_date, datetime.date(2015, 01, 01))
        self.assertEqual(obj.department_id, 1)

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

        self.assertFalse(self.model_cls.objects.filter(pk=self.pk).exists())

    def test_delete_view_post_ajax_invalid(self):
        page_url = self.models_urls['delete'] % 999
        expected_status_code = 404

        response = self.client.post(page_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertStatusCodeEqual(response, expected_status_code, msg_postfix='URL: %s' % page_url)
