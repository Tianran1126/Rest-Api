from Api.resource import pokemon
from flask import Blueprint
from flask import Flask, request, jsonify, make_response   
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from . import app
from . import db 
from .models import User

auth=Blueprint('auth',__name__)

@auth.route('/register',methods=['GET','POST'])
def register():
  """register information of the user to the database

  Returns:
      [type]: return registered successfully message
  """

  data=request.get_json()
  password_hashed=generate_password_hash(data['password'],method='sha256')
  user=User.query.get(data['username'])
  if user:
    return ({'409':'username is taken'})
  new_user = User(username=data['username'], password=password_hashed) 
  db.session.add(new_user)  
  db.session.commit()    
  return jsonify({'message': 'registered successfully'}) 

#401-> The request can't not been appiled beacuse it lacks valid credentials for the resource 
@auth.route('/login')   
def give_toekn():  
  """ give the token to the user if user's infomraton is in the database
     the token lasts 40 min
  Returns:
      [type]: return the token to the user
  """
  auth=request.authorization
  user = User.query.get(auth.username)

  if not auth or not auth.username or not auth.password or not user:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({'username': user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=40)},"secret",algorithm="HS256")  
     return jsonify({'token' : token}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

