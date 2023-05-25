#!/usr/bin/penv python3
""" encrypts a password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ retunes a salted has of the input string """
    pasw = str.encode(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pasw, salt)
