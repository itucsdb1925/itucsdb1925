from flask import Flask,render_template,request,redirect,flash,url_for
import psycopg2 as dbapi2
from balance import Balance
from user import User,get_user
from database import Database
from forms import SigninForm
from flask_login import LoginManager,login_user,logout_user,login_required

f = open("database_string.txt","r")
dsn = f.read()
#@app.route("/signin",methods=["POST","GET"])
def sign_in():
  form = SigninForm()
  if form.validate_on_submit():
    username = form.data["username"]
    password = form.data["password"]
    user = get_user(username)
    database=Database(dsn)
    database.create_user()
    print(user.user_name,user.password)
    if(username and password):
      if(user.password):
        if(database.verify_user(password,user.password)):
          login_user(user)
          flash("You have logged in.")
          return redirect("/signedin")
      flash("Invalid credentials.")
  return render_template("signin.html",form=form)

@login_required
def sign_out():
  logout_user()
  flash("You have logged out.")
  return redirect(url_for("sign_in"))

#@app.route("/signup",methods=["POST","GET"])
def sign_up():
  username = request.form.get("username")
  password = request.form.get("password")
  database=Database(dsn)
  database.create_user()
  if(username and password):
    user=User(username,password)
    database.add_user(user)
    next_page = request.args.get("next", url_for("/signedin"))
    return redirect(next_page)
  return render_template("signup.html")

#@app.route("/update", methods=["POST","GET"])
@login_required
def update():
  update_id = request.form.get("id_to_update")
  num1 = request.form.get("Cash_update")
  num2 = request.form.get("MobyCoin_update")
  given_name = request.form.get("Name_update")
  if(num1 and num2):
    num1=float(num1)
    num2=float(num2)
  database=Database(dsn)
  database.create_balance()
  if(num1 and num2 and update_id and given_name):
    update_balance = Balance(update_id,given_name,num1,num2)
    database.update_balance(update_balance)
    return redirect("/signedin")
  return render_template("update.html",update_id=update_id)

#@app.route("/signedin", methods=["POST","GET"])
@login_required
def home_page():
  num1 = request.form.get("Cash")
  num2 = request.form.get("MobyCoin")
  given_name = request.form.get("Name")
  delete_id = request.form.get("id_to_delete")
  update_id = request.form.get("id_to_update")
  if(num1 and num2):
    num1=float(num1)
    num2=float(num2)
  database=Database(dsn)
  database.create_balance()
  if(delete_id):
    database.delete_balance(delete_id)
  """if(update_id):
    return redirect(url_for("update",update(update_id)))"""
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
