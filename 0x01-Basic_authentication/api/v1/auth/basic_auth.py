#!/use/bin/env python3
""" a module for the basic_auth class """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ expand the Auth class """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ returns Base64 part of authorization header """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None

        head_list = authorization_header.split()
        if head_list[0] != 'Basic':
            return None
        else:
            return head_list[1]
