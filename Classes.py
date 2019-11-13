from flask import *
import psycopg2 as dbapi2
import names

class Balance:
  def __init__(self, Id, Name, Cash=0, MobyCoin=0):
    self.id = Id
    self.name = Name
    self.cash = Cash
    self.mobyCoin = MobyCoin
    
class Database:
  def __init__(self, connection_string):
    self.connection_string = connection_string
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
      cursor.close()