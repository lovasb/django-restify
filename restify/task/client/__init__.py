# coding: utf-8

from requests import Request, Session, PreparedRequest

from typing import Dict

from restify.task.client.authentication import ClientAuthenticationBase


class Client:
    def __init__(self, api: str, auth_object: ClientAuthenticationBase):
        self.api = api

        self.session = Session()
        self.auth_object = auth_object

    def _prepare(self, signature: Dict) -> PreparedRequest:
        request = Request('POST', self.api, json=signature)

        self.auth_object.inject_credentials(request)

        return self.session.prepare_request(request)

    def _send(self, request: PreparedRequest):
        self.session.send(request)

    def call(self, name, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        request = self._prepare({
            'function': name,
            'args': args,
            'kwargs': kwargs
        })

        response = self._send(request)
        # TODO: Continue here
