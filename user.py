from flask import Flask
import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin
from database import Database

dsn = os.getenv("DATABASE_URL")

class User(UserMixin):
  def __init__(self, User_name, Password,Balance_id=0):
    self.user_name = User_name
    self.password = Password
    self.active = True

  def get_id(self):
    return self.user_name

  @property
  def is_active(self):
    return self.active
def get_user(user_id):
  database=Database(dsn)
  password = database.get_hashed_password(user_id)[0] if database.get_hashed_password(user_id) else None
  user = User(user_id, password) if password else None
  return user