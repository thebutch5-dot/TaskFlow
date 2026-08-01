from datetime import datetime
from peewee import Model, CharField, TextField, BooleanField, DateTimeField, ForeignKeyField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel, UserMixin):
    username = CharField(unique=True, max_length=60)
    email = CharField(unique=True, max_length=120)
    password_hash = CharField(max_length=255)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(BaseModel):
    title = CharField(max_length=100)
    description = TextField(null=True)
    priority = CharField(max_length=20, default='Medium')
    is_completed = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.now)

    user = ForeignKeyField(User, backref='tasks', on_delete='CASCADE')

