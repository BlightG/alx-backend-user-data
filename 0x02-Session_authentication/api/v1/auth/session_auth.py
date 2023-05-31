#!/usr/bin/env python3
""" a module for the SessionAuth class """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid

class SessionAuth(Auth):
    """ a class session based Authentication """
    
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session id for a user id """
        if user_id is None or not isinstance(user_id, str):
            return None
        
        user_session = str(uuid.uuid4())
        self.user_id_by_session_id[user_session] = user_id
        return user_session

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user id based on session id """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """ returns current users based on cookie value """

        if request is None:
            return None

        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        
        user = self.user_id_for_session_id(cookie)
        if user is None:
            return None

        return User.get(user)

    def destroy_session(self, request=None):
        """ deletes a session """

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
        