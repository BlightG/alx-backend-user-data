#!/usr/bin/env python3
""" an AUTH module """
import bcrypt
from db import DB
from user import User
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
        if self._db._session.query(User).first() is None:
            usr = self._db.add_user(u_email, hash)
            return usr

        kwarg = {'email': u_email}
        try:
            obj = self._db.find_user_by(**kwarg)
            raise ValueError(f'User {u_email} already exists')
        except NoResultFound:
            usr = self._db.add_user(u_email, hash)
            return usr
