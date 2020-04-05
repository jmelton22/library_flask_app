#!/usr/bin/env python3
from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from app import db

Base = automap_base()


class User(UserMixin, Base, db.Model):
    __tablename__ = 'User'

    def get_id(self):
        return self.user_id


class Book(Base, db.Model):
    __tablename__ = 'Book'


class Author(Base, db.Model):
    __tablename__ = 'Author'


class Genre(Base, db.Model):
    __tablename__ = 'Genre'


class UserBook(Base, db.Model):
    __tablename__ = 'UserBook'


class Library(Base, db.Model):
    __tablename__ = 'Library'


class LibraryCatalog(Base, db.Model):
    __tablename__ = 'LibraryCatalog'


class Admin(Base, db.Model):
    __tablename__ = 'Admin'


Base.prepare(db.engine, reflect=True)
