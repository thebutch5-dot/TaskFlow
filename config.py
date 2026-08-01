import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
    DATABASE_PATH = os.path.join('instance', 'taskflow.db')
    import os

    class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
        DATABASE_PATH = os.path.join('instance', 'taskflow.db')
