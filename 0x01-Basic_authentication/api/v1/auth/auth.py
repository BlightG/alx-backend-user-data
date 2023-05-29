#!/usr/bin/env python3
""" a module for the Auth class """
import request
from typing import List, TypeVar
from flask import Flask



class Auth:
    """ a class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ requires auth """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorizes header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None
    
    