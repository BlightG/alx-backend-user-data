#!/usr/bin/env python3
""" an AUTH module """
import bcrypt
from db import DB
from user import User
import uuid
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ has password """
    if password is None or not isinstance(password, str):
        return None

    b_pass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(b_pass, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, u_email: str, u_password: str):
        """ used to register a user """
        if u_email is None or not isinstance(u_email, str):
            return None

        if u_password is None or not isinstance(u_password, str):
            return None

        b_hash = _hash_password(u_password)
        hash = b_hash.decode('utf-8')

        kwarg = {'email': u_email}
        try:
            obj = self._db.find_user_by(**kwarg)
            raise ValueError(f'User {obj.email} already exists')
        except NoResultFound:
            usr = self._db.add_user(u_email, hash)
            return usr

    def valid_login(self, u_email: str, u_password: str) -> bool:
        """ verifies the password """

        if u_email is None or not isinstance(u_email, str):
            return None

        if u_password is None or not isinstance(u_password, str):
            return None

        kwarg = {'email': u_email}
        try:
            usr = self._db.find_user_by(**kwarg)
            if usr.email == u_email:
                b_pass = usr.hashed_password.encode('utf-8')
                b_hash = u_password.encode('utf-8')
                return bcrypt.checkpw(b_hash, b_pass)
            return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """ generates a uuid string """
        return str(uuid.uuid4())

    def create_session(self, u_email: str) -> str:
        """ returns an id for a session """

        if u_email is None or not isinstance(u_email, str):
            return None
        
        kwarg = {'email': u_email}
        try:
            usr = self._db.find_user_by(**kwarg)
            session = self._generate_uuid()
            self._db.update_user(usr.id, session_id = session)
            return session
        except NoResultFound:
            return None

    def get_user_from_session_id(self, u_session: str) -> User:
        """ returns a user from session id """

        if u_session is None or not isinstance(u_session, str):
            return None

        try:
            usr = self._db.find_user_by(session_id=u_session)
            return usr
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """ destroyes a session_id of a user class """
        if user_id is None or not isinstance(user_id, int):
            return None

        kwargs = {'id': user_id}
        try:
            usr = self._db.find_user_by(**kwargs)
            self._db.update_user(usr.id, session_id = None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, u_email: str) -> str:
        """ used to reset the password """

        if u_email is None or not isinstance(u_email, str):
            return None

        try:
            usr = self._db.find_user_by(email=u_email)
            token = self._generate_uuid()
            self._db.update_user(usr.id, reset_token = token)
        except NoResultFound:
            raise ValueError