import os


class  Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://morrison:5431140@localhost/myblog'
  UPLOADED_PHOTOS_DEST ='app/static/photos'
  QUOTES_API ='http://quotes.stormconsultancy.co.uk/random.json'
  
class  ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
  if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",1)


class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://morrison:5431140@localhost/myblog'
  DEBUG = True
  
class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://morrison:5431140@localhost/test_myblog'
  pass

config_options = {
  'development':DevConfig,
  'production':ProdConfig,
  'test':TestConfig
}    