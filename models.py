#!/usr/bin/env python3
from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from app import db

Base = automap_base()


class User(UserMixin, Base, db.Model):
    __tablename__ = 'user'


class Book(Base, db.Model):
    __tablename__ = 'book'


class Author(Base, db.Model):
    __tablename__ = 'author'


class UserBook(Base, db.Model):
    __tablename__ = 'userbook'


Base.prepare(db.engine, reflect=True)
