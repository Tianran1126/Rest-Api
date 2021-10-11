from flask_restful import Resource, abort,reqparse, fields,marshal_with
from . import db
from .models import Pokemon
from flask import  request, jsonify
import jwt
from functools import wraps
from . import db 
from .models import User

def check_type(value):
  """check if the user posts "fire"or "water" or "grass" or "electric"
     for the type of the pokemon 

  Args:
      value ([type]): the type of the pokemon 

 Raises:
      ValueError: [description]

  Returns:
      [type]: return the correct type 
   """
  types = ["fire", "water", "grass","electric"]
  if value in types:
      return value
  raise ValueError("Correct types are fire,water,grass,electrcity")   

def check_name(value):
  """check if username exists in database

  Args:
      value ([type]): username

  Raises:
      ValueError: [description]

  Returns:
      [type]: return the correct username 
  """
  current_user=User.query.get(value) 
  if current_user:
      return value
  raise ValueError("The  username does not exist")   

    
parser=reqparse.RequestParser()
parser.add_argument("name",type=str,help="the name of the pokemon is required",required=True)
parser.add_argument("type",type=check_type,required=True)

resoruce_fields={"id":fields.Integer,"name":fields.String,
"type":fields.String}

def find_pokemon(pokemon_id):
  """ find the pokemon in the database using the the id of the pokemon  

  Args:
      pokemon_id ([type]): id of the pokemon 

  Returns:
      [type]: return the pokemon 
  """
  return Pokemon.query.filter_by(id=pokemon_id).first()

def abort_pokemon_non_exist(pokemon):
  """display a messga e for the user if pokemon doesn't exist in the database

  Args:
      pokemon ([type]): [description]
  """
  if not pokemon:
      abort(404,message="pokemon don't exist")

def token_required(f):
  """check if user has the correct token
  """
  @wraps(f)
  def decorator(*args,**kwargs):
    token=None

    if 'x-access-tokens' in request.headers:
      token=request.headers['x-access-tokens']

    if not token:
      return({'message':'a valid token is missing '})  

    try:  
          data=jwt.decode(token,"secret", algorithms=["HS256"])
          current_user = User.query.get(data['username'])  
          
    except:  
          return jsonify({'message': 'token is invalid'})  

    return f(current_user, *args,  **kwargs)  
    
  return decorator 


class pokemon(Resource):
  
  @marshal_with(resoruce_fields)
  def get(self,pokemon_id):
    """ get the infomration of a pokemon from database

    Args:
        pokemon_id ([type]): id of the pokemon


    """
    pokemon=find_pokemon(pokemon_id)
    abort_pokemon_non_exist(pokemon)
    return pokemon  
  
  @marshal_with(resoruce_fields)
  @token_required
  def post(self,current_user,pokemon_id):
    """ post the infomration of a pokemon to the database

    Args:
        pokemon_id ([type]): id of the pokemon

    """
    args=parser.parse_args()
    if find_pokemon(pokemon_id):
      abort(409,message="video_id taken")
    pokemon=Pokemon(id=pokemon_id,name=args['name'],type=args['type'])

    db.session.add(pokemon)
    db.session.commit()
    return pokemon,201

  @marshal_with(resoruce_fields)
  @token_required
  def delete(self,current_user,pokemon_id):
    """ delete the infomration of a pokemon from the database

    Args:
        pokemon_id ([type]): id of the pokemon

    """
    pokemon=find_pokemon(pokemon_id)
    abort_pokemon_non_exist(pokemon)
    db.session.delete(pokemon)
    db.session.commit()
    return pokemon,204






