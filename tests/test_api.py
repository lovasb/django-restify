from django.apps import apps
from django.test import TestCase
from django.urls import URLPattern

from restify.api import Api
from restify.resource import Resource


class CustomResource(Resource):
    class Meta:
        resource_name = 'example'


class ApiTest(TestCase):
    def test_api_naming(self):
        api = Api()
        self.assertEqual(api.name, 'v1')
        api = Api(api_name='v2')
        self.assertEqual(api.name, 'v2')

    def test_api_urls_empty(self):
        api = Api()
        urls, app_name = api.urls
        self.assertEqual(app_name, apps.get_app_config('restify').name)

        self.assertEqual(len(urls), 0)
        self.assertIsInstance(urls, list)

    def test_api_register_resource(self):
        api = Api()
        api.register(r'first/$', CustomResource)
        urls, app_name = api.urls
        self.assertEqual(app_name, apps.get_app_config('restify').name)

        url, = urls
        self.assertIsInstance(url, URLPattern)
        self.assertEqual(url.name, 'example')
