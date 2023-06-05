#!/usr/bin/env python3
""" a class user for to instansiate user table """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hased_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))