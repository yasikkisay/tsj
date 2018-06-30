import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    city = CharField()
    street = CharField()
    house_number = IntegerField()
    flat_number = IntegerField()
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        CompositeKey = ('city', 'street', 'house_number', 'flat_number')

    def get_user_statistic(self):
        return UsersStatistics.select().where(UsersStatistics.user == self)

    @classmethod
    def create_user(cls, username, email, password, city, street, house_number, flat_number, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    city=city,
                    street=street,
                    house_number=house_number,
                    flat_number=flat_number,
                    is_admin=admin)
        except IntegrityError:
            raise ValueError('User already exist')


class UsersStatistics(Model):
    user = ForeignKeyField(
        rel_model=User,
        related_name='statistics'
    )
    post_created = DateTimeField(default=datetime.datetime.now)
    interval = DateField()
    hot_water = IntegerField()
    cold_water = IntegerField()
    gas = IntegerField()
    electricity = IntegerField()

    class Meta:
        database = DATABASE
        order_by = ('-post_created',)

    @classmethod
    def add_fee(cls, user, interval, hot_water, cold_water, gas, electricity):
        try:
            with DATABASE.transaction():
                cls.create(
                    user=user,
                    interval=interval,
                    hot_water=hot_water,
                    cold_water=cold_water,
                    gas=gas,
                    electricity=electricity
                )
        except IntegrityError:
            raise ValueError('Несоответствие введенных данных данным в базе.')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, UsersStatistics], safe=True)
    DATABASE.close()
