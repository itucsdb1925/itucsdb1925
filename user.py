from flask import *
import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, User_name, Password):
    self.user_name = User_name
    self.password = hasher.hash(Password)
    self.active = True
    self.is_admin = False

  def get_id(self):
    return self.user_name

  @property
  def is_active(self):
    return self.active