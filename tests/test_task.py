# coding: utf-8

from django.test import TestCase

from restify.task import api_task, fullname, NameConflict


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

        self.assertIs(f, api_task(f)(f))
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
        @api_task
        def f(): pass
        task_name = fullname(f)

        api_task.call(task_name)

        api_task.remove(f)
        self.assertRaises(KeyError, lambda: api_task.call(task_name))
