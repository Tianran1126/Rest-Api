from . import db 

class User(db.Model):
  username=db.Column(db.String(50),primary_key=True)
  password=db.Column(db.String(150)) 

class Pokemon(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(80))
  type=db.Column(db.String(50))



 
  


