from flask import *
import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin

class Balance:
  def __init__(self, Id, Name, Cash=0, MobyCoin=0):
    self.id = Id
    self.name = Name
    self.cash = Cash
    self.mobyCoin = MobyCoin