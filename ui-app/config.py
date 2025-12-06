import os

class Config:
    # SECRET_KEY fallback
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')

    # Database URL from environment or default local value
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        "postgresql://postgres:password@127.0.0.1:5432/my_local_db"
    )
