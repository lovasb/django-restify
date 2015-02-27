from django.test import TestCase

from restify.http.response import ApiResponse
from restify.serializers import BaseSerializer
from restify import status


class ApiResponseTest(TestCase):
    def test_serializaton(self):
        data = {'example': 'data'}
        resp = ApiResponse(data, serializer=BaseSerializer)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.content, b'"{\\"example\\": \\"data\\"}"')