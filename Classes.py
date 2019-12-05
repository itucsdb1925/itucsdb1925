from flask import *
import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher

class User:
  def __init__(self, User_name, Password):
    self.user_name = User_name
    self.password = hasher.hash(Password)

class Balance:
  def __init__(self, Id, Name, Cash=0, MobyCoin=0):
    self.id = Id
    self.name = Name
    self.cash = Cash
    self.mobyCoin = MobyCoin
    
class Database:
  def __init__(self, connection_string):
    self.connection_string = connection_string
  def create_user(self):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="CREATE TABLE IF NOT EXISTS USERS (USER_NAME VARCHAR(100) PRIMARY KEY, PASSWORD VARCHAR(1000))"
      cursor.execute(sql_command)
      connection.commit()
      cursor.close()
  def add_user(self,user):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="INSERT INTO USERS (USER_NAME,PASSWORD) VALUES (%(user_name)s, %(password)s)"
      cursor.execute(sql_command,{'user_name':user.user_name,'password':user.password})
      connection.commit()
      cursor.close()
  def get_hashed_password(self,name):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="SELECT PASSWORD FROM USERS WHERE(USER_NAME = %(user_name)s)"
      cursor.execute(sql_command,{'user_name':name})
      hashed_password = cursor.fetchone()
      connection.commit()
      cursor.close()
    return hashed_password
  def verify_user(self,password,hashed_password):
    return(hasher.verify(password,hashed_password))
  def create_balance(self):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="CREATE TABLE IF NOT EXISTS BALANCE (ID SERIAL PRIMARY KEY, NAME VARCHAR(100), CASH FLOAT, MOBYCOIN FLOAT)"
      cursor.execute(sql_command)
      connection.commit()
      cursor.close()
  def get_balance(self,balance_id):
    balance_data = []
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="SELECT * FROM BALANCE WHERE(ID = %(id)s)"
      cursor.execute(sql_command,{'id':balance_id})
      balance_data = cursor.fetchone()
      connection.commit()
      cursor.close()
    return Balance(balance_data[0],balance_data[1],balance_data[2],balance_data[3])
  def add_balance(self,balance):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="INSERT INTO BALANCE (NAME,CASH,MOBYCOIN) VALUES (%(name)s, %(cash)s, %(mobycoin)s)"
      cursor.execute(sql_command,{'name':balance.name,'cash':balance.cash,'mobycoin':balance.mobyCoin})
      connection.commit()
      cursor.close()
  def delete_balance(self,balance):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command_get_id="SELECT ID FROM BALANCE WHERE(NAME = %(name)s AND CASH = %(cash)s AND MOBYCOIN = %(mobycoin)s)"
      cursor.execute(sql_command_get_id,{'name':balance.name,'cash':balance.cash,'mobycoin':balance.mobyCoin})
      del_balance_id = cursor.fetchone()
      cursor.close()
      cursor = connection.cursor()
      sql_command="DELETE FROM BALANCE WHERE (ID = %(id)s)"
      cursor.execute(sql_command,{'id':del_balance_id})
      connection.commit()
<<<<<<< HEAD
      cursor.close()
  def update_balance(self,balance):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command_get_id="SELECT ID FROM BALANCE WHERE(NAME = %(name)s AND CASH = %(cash)s AND MOBYCOIN = %(mobycoin)s)"
      cursor.execute(sql_command_get_id,{'name':balance.name,'cash':balance.cash,'mobycoin':balance.mobyCoin})
      update_balance_id = cursor.fetchone()
      cursor.close()
      cursor = connection.cursor()
      sql_command="UPDATE BALANCE SET NAME=%(id)s,CASH = %(cash)s,MOBYCOIN = %(mobycoin)s WHERE (ID = %(id)s)"
      cursor.execute(sql_command,{'name':balance.name,'cash':balance.cash,'mobycoin':balance.mobyCoin,'id':update_balance_id})
      connection.commit()
=======
>>>>>>> 97eea31c378a621aa335f17a3c658038a5bfa5cc
      cursor.close()