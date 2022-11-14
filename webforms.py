from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, input_required, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


# create a search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a posts form
class PostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content',validators=[DataRequired()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email?", validators=[DataRequired()])
    password_hash = PasswordField("What's Your password?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField(
        'Password', validators=[DataRequired(), 
        EqualTo('password_hash2', 
        message='passwords must match')]
        )
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")
