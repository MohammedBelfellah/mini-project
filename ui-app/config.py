import os

class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@localhost:5432/urban_heritage'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'