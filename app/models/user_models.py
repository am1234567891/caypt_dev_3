# Copyright 2019 Stemfellowship
#
# Authors: Andrew Mao

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, DateField, SelectField, TextField, TextAreaField
from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    # active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    institution = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    pnumber = db.Column(db.String(30), nullable=False)
    background = db.Column(db.String(255), nullable=False)
    dietary_restriction = db.Column(db.String(255), nullable=False)
    tshirt_size = db.Column(db.String(20), nullable=False)
    mailing_address = db.Column(db.String(255))
    physics_background = db.Column(db.String(255))   # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
class CustomRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    dob = DateField('Date of birth (yyyy-mm-dd)', validators=[
        validators.DataRequired('Date of birth is required')])
    pnumber = StringField('Phone number', validators=[
        validators.DataRequired('Phone number is required')])
    institution = StringField('Institution', validators=[
        validators.DataRequired('Institution is required')])
    physics_background = TextAreaField('Physics background (Maximum 250 characters)')
    mailing_address = TextAreaField('Mailing address', validators=[
        validators.DataRequired('Mailing address is required')])
    dietary_restriction = StringField('Health and Dietary Concerns')
    tshirt_size = SelectField('T-shirt size',
        choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')])
    background = SelectField('Education Background',
                              choices=[('10', 'Middle School'), ('12', 'High School'), ('20', 'Under Graduate or above')]
    )
    submit = SubmitField('Submit and Accept Terms')


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    dob = DateField('Date of birth (yyyy-mm-dd)', validators=[
        validators.DataRequired('Date of birth is required')])
    pnumber = StringField('Phone number', validators=[
        validators.DataRequired('Phone number is required')])
    institution = StringField('Institution', validators=[
        validators.DataRequired('Institution is required')])
    physics_background = TextAreaField('Physics Background (Maximum 250 characters)')
    mailing_address = TextAreaField('Mailing address', validators=[
        validators.DataRequired('Mailing address is required')])
    background = SelectField('Education Background',
                              choices=[('10', 'Middle School'), ('12', 'High School'), ('20', 'Under Graduate or above')]
    )
    dietary_restriction = StringField('Health and Dietary Concerns')
    tshirt_size = SelectField('T-shirt size',
        choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')]
    )

    submit = SubmitField('Save')


class CustomUserProfileForm(UserProfileForm):
    institution = StringField('Institution')
    dob = DateField('Date of birth')
