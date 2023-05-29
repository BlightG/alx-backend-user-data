#!/use/bin/env python3
""" a module for the basic_auth class """
from .auth import Auth
from models.user import User
from typing import TypeVar
import base64
import binascii

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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ decodes an str encoded base_64 object """

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        bytes64 = bytes(base64_authorization_header, "utf-8")
        try:
            return base64.b64decode(bytes64).decode("utf-8")
        except binascii.Error:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns ussername and value from base64 """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        auth64 = decoded_base64_authorization_header.split(":")

        return (auth64[0], auth64[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns user instance based on email and password """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        if len(User.search({'email': user_email})) == 0:
            return None
        else:
            u_list = User.search({'email': user_email})

        u = u_list[0]
        if u.is_valid_password(user_pwd) is False:
            return None
        else:
            return u

    def current_user(self, request=None) -> TypeVar('User')
        """ user instance of a request """
        
        