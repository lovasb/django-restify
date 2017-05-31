# coding: utf-8

from unittest.mock import call, patch, MagicMock

from django.test import TestCase

from restify.task.client import Client, ClientException, RemoteException, UnexpectedFormatException


class ClientExceptionTests(TestCase):
    def test_init(self):
        mock_response = MagicMock()

        e = ClientException(mock_response)
        self.assertIs(e.response, mock_response)


class UnexpectedFormatExceptionTests(TestCase):
    def test_init(self):
        self.assertTrue(issubclass(UnexpectedFormatException, ClientException))


class RemoteExceptionTests(TestCase):
    def test_init(self):
        mock_response = MagicMock(**{'json.return_value': None})

        self.assertRaises(UnexpectedFormatException, lambda: RemoteException(mock_response))

        mock_response.json.return_value = {
            'exception': 'EXCEPTION'
        }

        e = RemoteException(mock_response)
        self.assertEqual(e.exception, 'EXCEPTION')

        self.assertEqual(
            str(e),
            '\n'
            '"""\n'
            'EXCEPTION'  # Note: There is no explicit \n here
            '"""'
        )


class ClientTests(TestCase):
    @patch('restify.task.client.Client._send')
    @patch('restify.task.client.Client._prepare')
    def test_call(self, mock_prepare: MagicMock, mock_send: MagicMock):
        mock_send.return_value = MagicMock(**{'json.return_value': {'return': 'RETVAL'}})

        client = Client('api', None, verify=False)
        retval = client.call('some_task', args=('arg0', ), kwargs={'kwarg0': 'value0'})

        self.assertEqual(retval, 'RETVAL')

        self.assertEqual(mock_prepare.mock_calls, [
            call({
                'function': 'some_task',
                'args': ('arg0', ),
                'kwargs': {'kwarg0': 'value0'}
            })
        ])

        self.assertEqual(mock_send.mock_calls, [
            call(mock_prepare.return_value),
            call().raise_for_status(),
            call().json()
        ])
