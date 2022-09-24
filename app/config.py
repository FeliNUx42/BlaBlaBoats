import os

class Config:
  DEBUG = True
  SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:5000")
  SECRET_KEY = os.environ.get("SECRET_KEY", "6a751e567934f9441cf948947d7ad63b")

  RES_PER_PAGE = 10
  PICTURES_FOLDER = "static/pictures"
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  MAX_TRIPS = 20

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "sqlite:///database.db")
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  SITEMAP_URL_SCHEME = "http"

  ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")

  STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
  STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

  MAPS_API_KEY = os.environ.get("MAPS_API_KEY")

  SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
  SENDGRID_EMAIL = os.environ.get("SENDGRID_EMAIL")