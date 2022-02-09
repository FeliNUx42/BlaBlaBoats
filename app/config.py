import os

class Config:
  DEBUG = True
  SECRET_KEY = os.environ.get("SECRET_KEY", "6a751e567934f9441cf948947d7ad63b")
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  PICTURES_FOLDER = "static/pictures"

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')\
    .replace('postgres://', 'postgresql://') or 'sqlite:///database.db'

  SQLALCHEMY_TRACK_MODIFICATIONS = False