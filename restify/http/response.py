#encoding: utf8
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


class ApiResponse(JsonResponse):
    def __init__(self, data, serializer, **kwargs):
        serialized = serializer().flatten(data)
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(serialized, cls=DjangoJSONEncoder)
        super(ApiResponse, self).__init__(data=data, safe=False, **kwargs)