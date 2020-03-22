#!/usr/bin/env python3
from sqlalchemy.ext.automap import automap_base
from app import db

Base = automap_base()


class User(Base):
    __tablename__ = 'user'


class Book(Base):
    __tablename__ = 'book'


class Author(Base):
    __tablename__ = 'author'


Base.prepare(db.engine, reflect=True)
