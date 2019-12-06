from flask import Flask
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin
from balance import Balance

class Database:
  def __init__(self, connection_string):
    self.connection_string = connection_string
  def create_user(self):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="CREATE TABLE IF NOT EXISTS USERS (USER_NAME VARCHAR(100) PRIMARY KEY, PASSWORD VARCHAR(100))"
      cursor.execute(sql_command)
      connection.commit()
      cursor.close()
  def add_user(self,user):
    user.password = hasher.hash(user.password)
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
      sql_command="CREATE TABLE IF NOT EXISTS BALANCE (ID SERIAL PRIMARY KEY, USER_NAME VARCHAR(100) REFERENCES USERS(USER_NAME),CASH FLOAT, MOBYCOIN FLOAT)"
      cursor.execute(sql_command)
      connection.commit()
      cursor.close()
  def get_balance(self,user_name):
    balance_data = []
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="SELECT * FROM BALANCE WHERE(USER_NAME = %(user_name)s)"
      cursor.execute(sql_command,{'user_name':user_name})
      balance_data = cursor.fetchone()
      connection.commit()
      cursor.close()
    return Balance(balance_data[0],balance_data[1],balance_data[2],balance_data[3])
  def add_balance(self,balance):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="INSERT INTO BALANCE (USER_NAME,CASH,MOBYCOIN) VALUES ( %(user_name)s, %(cash)s, %(mobycoin)s)"
      cursor.execute(sql_command,{'user_name':balance.user_name,'cash':balance.cash,'mobycoin':balance.mobyCoin})
      connection.commit()
      cursor.close()
  def delete_balance(self,balance_id):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="DELETE FROM BALANCE WHERE (ID = %(id)s)"
      cursor.execute(sql_command,{'id':balance_id})
      connection.commit()
      cursor.close()
  def update_balance(self,balance):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="UPDATE BALANCE SET CASH = %(cash)s,MOBYCOIN = %(mobycoin)s WHERE (ID = %(id)s)"
      cursor.execute(sql_command,{'cash':balance.cash,'mobycoin':balance.mobyCoin,'id':balance.id})
      connection.commit()
      cursor.close()
  def buy_mobycoin(self,balance,cash):
    if(cash>balance.cash):
      return False
    added_coin = cash / 10
    balance.mobyCoin += added_coin
    balance.cash -= cash
    self.update_balance(balance)
  def sell_mobycoin(self,balance,mobycoin):
    if(mobycoin>balance.mobyCoin):
      return False
    added_cash = mobycoin*10
    balance.mobyCoin -= mobycoin
    balance.cash += added_cash
    self.update_balance(balance)
  def transfer_between_users_cash(self,balance_src,balance_dst,cash):
    if(cash>balance_src.cash):
      return False
    balance_src.cash -= cash
    balance_dst.cash += cash
    self.update_balance(balance_src)
    self.update_balance(balance_dst)
  def transfer_between_users_mobycoin(self,balance_src,balance_dst,mobycoin):
    if(mobycoin>balance_src.mobyCoin):
      return False
    balance_src.mobyCoin -= mobycoin
    balance_dst.mobyCoin += mobycoin
    self.update_balance(balance_src)
    self.update_balance(balance_dst)