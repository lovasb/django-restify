# coding: utf-8

from requests import Request


class ClientAuthenticationBase:
    def inject_credentials(self, request: Request) -> None:
        raise NotImplementedError('Subclass must implement this')
