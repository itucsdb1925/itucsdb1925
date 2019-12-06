import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin

class Balance:
  def __init__(self, Id,User_name, Cash=0, MobyCoin=0):
    self.id = Id
    self.user_name = User_name
    self.cash = Cash
    self.mobyCoin = MobyCoin
    