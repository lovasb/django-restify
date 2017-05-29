# coding: utf-8

import json
from unittest.mock import call, patch, MagicMock

from django.test import TestCase, RequestFactory

from restify.task import api_task, fullname, NameConflict
from restify.task.resource import TaskResource


class MockGlobalClass:
    pass


class DebugTests(TestCase):
    def test_fullname(self):
        class MockLocalClass:
            pass

        self.assertEqual(fullname(MockGlobalClass), 'tests.test_task.MockGlobalClass')
        self.assertEqual(fullname(MockLocalClass), 'tests.test_task.DebugTests.test_fullname.<locals>.MockLocalClass')


class ApiTaskTests(TestCase):
    def tearDown(self):
        api_task._registry = {}

    def test_decorator(self):
        def f(): pass

        self.assertIs(f, api_task(f))
        self.assertIs(f, api_task('f_2')(f))

    def test_add(self):
        def f(): pass

        self.assertRaisesRegex(
            ValueError, "name must be a str, got <class 'int'> instead",
            lambda: api_task.add(f, 1)
        )

        api_task.add(f, 'task_f')

        self.assertRaises(NameConflict, lambda: api_task.add(f, 'task_f'))

    def test_remove(self):
        @api_task()
        def f(): pass
        task_name = fullname(f)

        api_task.call(task_name)

        api_task.remove(f)
        self.assertRaises(KeyError, lambda: api_task.call(task_name))

    def test_prepare_remote_call(self):
        self.assertEqual(api_task.prepare_remote_call('function', 'arg0', kwarg0='value0'), {
            'function': 'function',
            'args': ('arg0', ),
            'kwargs': {
                'kwarg0': 'value0'
            }
        })

    @patch('restify.task.TaskRegistry.call')
    def test_dispatch_remote_call(self, mock_call: MagicMock):
        api_task.dispatch_remote_call({
            'function': 'function',
            'args': ('arg0', ),
            'kwargs': {
                'kwarg0': 'value0'
            }
        })

        self.assertEqual(mock_call.mock_calls, [
            call('function', 'arg0', kwarg0='value0')
        ])


class TaskResourceTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def tearDown(self):
        api_task._registry = {}

    def test_post_exception(self):
        resource = TaskResource.as_callable()

        request = self.rf.post('/')
        response = resource(request)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        self.assertIn('Traceback', content['exception'])

    def post(self):
        @api_task(name='echo')
        def echo(*args, **kwargs):
            return args, kwargs

        resource = TaskResource.as_callable()

        request = self.rf.post('/')
        request.POST = {
            'function': 'echo',
            'args': ('arg0', ),
            'kwargs': {'kwarg0': 'value0'}
        }
        response = resource(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content, json.dumps({
            'return': [
                ['arg0'],
                {'kwarg0': 'value0'}
            ]
        }).encode())
