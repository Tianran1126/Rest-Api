from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from os import path


app=Flask(__name__)
app.config['SECRET_KEY']='1234'
db=SQLAlchemy(app)

def create_app():
  api=Api(app)

  app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
  from .models import User,Pokemon
  from .auth import auth 
  from .resource import pokemon
  make_database(app)
  app.register_blueprint(auth,url_prefix='/')
  api.add_resource(pokemon,"/pokemon/<int:pokemon_id>")
  return app 


def make_database(app):
  if not path.exists('Api/database.db'):
     db.create_all(app=app)
