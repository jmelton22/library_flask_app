#!/usr/bin/env python3

import os


class Config:
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    HOSTNAME = os.environ['HOSTNAME']
    DATABASE = os.environ['DATABASE']

    SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ['SECRET_KEY']
