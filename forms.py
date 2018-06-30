from flask_wtf import FlaskForm
from models import User
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField,
                     DateField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length,
                                EqualTo, InputRequired)


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


def address_exists(form, field):
    raise ValidationError('Пользователь с данным адресом уже существует.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Username should be with words, letters, numbers and underscores only.'
            ),
            name_exists
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', 'Password must match.')
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[
            DataRequired()
        ]
    )
    city = StringField(
        'Город',
        validators=[
            DataRequired(),
            Length(max=25)
        ]
    )
    street = StringField(
        'Улица',
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )
    house_number = IntegerField(
        'Номер дома',
        validators=[
            DataRequired()
        ]
    )
    flat_number = IntegerField(
        'Номер квартиры',
        validators=[
            DataRequired()
        ]
    )


class FeesForm(FlaskForm):
    interval = DateField(
        'Укажите отчетный месяц',
        validators=[
            DataRequired()
        ],
        format='%Y-%m'
    )
    hot_water = IntegerField(
        'Показания горячей воды',
        validators=[
            InputRequired()
        ]
    )
    cold_water = IntegerField(
        'Показания холоднрй воды',
        validators=[
            InputRequired()
        ]
    )
    gas = IntegerField(
        'Показания газа',
        validators=[
            InputRequired()
        ]
    )
    electricity = IntegerField(
        'Показания электроэнергии',
        validators=[
            InputRequired()
        ]
    )
