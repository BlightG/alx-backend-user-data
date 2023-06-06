#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from db import DB

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

session = auth.create_session(email)
print(session)

usr = auth.get_user_from_session_id(session)

session_1 = auth.create_session(email)
print(session_1)

auth.destroy_session(usr.id)
print(usr.session_id)