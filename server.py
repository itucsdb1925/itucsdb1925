from flask import *
import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin
from balance import Balance
from user import User
from database import Database

app = Flask(__name__)

@app.route("/signin",methods=["POST","GET"])
def sign_page():
  username = request.form.get("username")
  password = request.form.get("password")
  dsn = """user='postgres' password='yattara'
  host='127.0.0.1' dbname='MobyCoin'"""
  database=Database(dsn)
  database.create_user()
  if(username and password):
    hashed_password = database.get_hashed_password(username)
    print(hashed_password)
    if(hashed_password):
      if(database.verify_user(password,hashed_password[0])==True):
        return redirect("/signedin")
  return render_template("signin.html")

@app.route("/signup",methods=["POST","GET"])
def sign_up():
  username = request.form.get("username")
  password = request.form.get("password")
  dsn = """user='postgres' password='yattara'
  host='127.0.0.1' dbname='MobyCoin'"""
  database=Database(dsn)
  database.create_user()
  if(username and password):
    user=User(username,password)
    database.add_user(user)
    return redirect("/signin")
  return render_template("signup.html")

@app.route("/update", methods=["POST","GET"])
def update(update_id):
  num1 = request.form.get("Cash_update")
  num2 = request.form.get("MobyCoin_update")
  given_name = request.form.get("Name_update")
  if(num1 and num2):
    num1=float(num1)
    num2=float(num2)
  dsn = """user='postgres' password='yattara'
  host='127.0.0.1' dbname='MobyCoin'"""
  database=Database(dsn)
  database.create_balance()
  if(update_id):
    balance_that_will_update = database.get_balance(update_id)
    database.update_balance(balance_that_will_update)
    return redirect("/signedin")
  return render_template("update.html")

  
@app.route("/signedin", methods=["POST","GET"])
def home_page():
  num1 = request.form.get("Cash")
  num2 = request.form.get("MobyCoin")
  given_name = request.form.get("Name")
  delete_id = request.form.get("id_to_delete")
  update_id = request.form.get("id_to_update")
  if(num1 and num2):
    num1=float(num1)
    num2=float(num2)
  dsn = """user='postgres' password='yattara'
  host='127.0.0.1' dbname='MobyCoin'"""
  database=Database(dsn)
  database.create_balance()
  if(delete_id):
    balance_that_will_delete = database.get_balance(delete_id)
    database.delete_balance(balance_that_will_delete)
  if(update_id):
    return redirect(url_for("update",update(update_id)))
  connection = dbapi2.connect(dsn)
  cursor = connection.cursor()
  if(num1 and num2):
    balance=Balance(0,given_name,num1,num2)
    database.add_balance(balance)
  statement="""SELECT * FROM BALANCE"""
  cursor.execute(statement)
  fetched = cursor.fetchall() 
  balance_list = []
  for i in fetched:
    balance_list.append(Balance(i[0],i[1],i[2],i[3]))
  #statement = """INSERT INTO PERSON (
  #NAME) VALUES (%(name_person)s)"""
  #cursor.execute(statement,{'name_person':names.get_full_name()})
  connection.commit()
  cursor.close()
  connection.close()
  return render_template("index.html",balance=balance_list,num=(num1,num2))


@app.route("/submit", methods=["POST"])
def submit():
    num1 = int(request.form.get("First Number"))
    num2 = int(request.form.get("Second Number"))
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>My movies</title>
  </head>
  <body>
    <h1>"""+ str(num1 + num2) +"""</h1>
  </body>
</html>
"""

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)
