import os
from peewee import SqliteDatabase
from config import Config

os.makedirs('instance', exist_ok=True)
db = SqliteDatabase(Config.DATABASE_PATH)

def get_user_by_id(user_id):
    from app.models import User
    try:
        return User.get_by_id(user_id)
    except Exception:
        return None

def get_user_by_username(username):
    from app.models import User
    return User.filter(User.username == username).first()

def get_user_by_email(email):
    from app.models import User
    return User.filter(User.email == email).first()

def create_user(username, email, password):
    from app.models import User
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def get_tasks_for_user(user_id):
    from app.models import Task
    return list(Task.select().where(Task.user_id == user_id).order_by(Task.date_created.desc()))

def get_task_by_id(task_id):
    from app.models import Task
    try:
        return Task.get_by_id(task_id)
    except Exception:
        return None

def add_new_task(title, description, priority, user_id):
    from app.models import Task
    task = Task.create(
        title=title,
        description=description,
        priority=priority,
        user_id=user_id
    )
    return task

def delete_task_from_db(task):
    task.delete_instance()

def toggle_task_status_in_db(task):
    task.is_completed = not task.is_completed
    task.save()



