#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[InputRequired()])
    library = SelectField('Library', validators=[InputRequired()], coerce=int)
    submit = SubmitField('Sign Up')


class AddBook(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    subtitle = StringField('Subtitle')
    first_name = StringField('Author First Name', validators=[InputRequired()])
    last_name = StringField('Author Last Name', validators=[InputRequired()])
    genre = SelectField('Genre', validators=[InputRequired()], coerce=int)
    submit = SubmitField('Add Book')


class EditProfile(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
    submit = SubmitField('Update Profile')
