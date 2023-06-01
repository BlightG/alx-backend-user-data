#!/usr/bin/env python3
""" a module for the SessionExpAuth class """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """ a classs to manage session expiration """

    def __init__(self):
        """ instanciates the class """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id: str = None):
        """ a function to create a session """
        session = super().create_session(user_id)
        if session is None:
            return None

        self.user_id_by_session_id[session] = {'user_id': user_id,
                                               'created_at': datetime.now()}
        return session

    def user_id_for_session_id(self, session_id=None):
        """ retrives a user by using the session id """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']

        if 'created_at' not in self.user_id_by_session_id[session_id].keys():
            return None

        created_at = self.user_id_by_session_id[session_id]['created_at']
        if created_at + self.session_duration < datetime.now():
            return None

        return self.user_id_by_session_id[session_id]['user_id']
