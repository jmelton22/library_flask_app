#!/usr/bin/env python3

import os


class Config:
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    HOSTNAME = os.environ['HOSTNAME']
    DATABASE = os.environ['DATABASE']
