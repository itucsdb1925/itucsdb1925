from flask import Flask,render_template,request,redirect,flash,url_for
import psycopg2 as dbapi2
from balance import Balance
from user import User,get_user
from database import Database
from forms import SigninForm
from flask_login import LoginManager,login_user,logout_user,login_required,current_user

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
    database.create_balance()
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
  database.create_balance()
  if(username and password):
    user=User(username,password)
    database.add_user(user)
    balance=Balance(0,username)
    database.add_balance(balance)
    next_page = request.args.get("next", url_for("sign_in"))
    return redirect(next_page)
  return render_template("signup.html")

#@app.route("/update", methods=["POST","GET"])
@login_required
def update():
  update_id = request.form.get("id_to_update")
  cash_update = request.form.get("Cash_update")
  mobycoin_update = request.form.get("MobyCoin_update")

  if(cash_update and mobycoin_update):
    cash_update=float(cash_update)
    mobycoin_update=float(mobycoin_update)
  database=Database(dsn)
  database.create_balance()
  if(cash_update and mobycoin_update and update_id):
    update_balance = Balance(update_id,"",cash_update,mobycoin_update)
    database.update_balance(update_balance)
    return redirect("/signedin")
  return render_template("update.html",update_id=update_id)

#@app.route("/signedin", methods=["POST","GET"])
@login_required
def home_page():
  user_id = current_user.get_id()
  user = get_user(user_id)
  cash = request.form.get("Cash")
  mobycoin = request.form.get("MobyCoin")
  #given_name = request.form.get("Name")
  delete_id = request.form.get("id_to_delete")
  update_id = request.form.get("id_to_update")
  database=Database(dsn)
  database.create_balance()
  if(cash):
    cash=float(cash)
    if(user):
      balance=database.get_balance(user_id)
      database.buy_mobycoin(balance,cash)
  if(mobycoin):
    mobycoin=float(mobycoin)
    if(user):
      balance=database.get_balance(user_id)
      database.sell_mobycoin(balance,mobycoin)
  if(delete_id):
    database.delete_balance(delete_id)
  """if(update_id):
    return redirect(url_for("update",update(update_id)))"""
  connection = dbapi2.connect(dsn)
  cursor = connection.cursor()
  #if(cash and mobycoin):
  #  balance=Balance(0,given_name,cash,mobycoin)
  #  database.add_balance(balance)
  statement="""SELECT * FROM BALANCE WHERE USER_NAME=%(user_name)s"""
  cursor.execute(statement,{'user_name':user.user_name})
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
  return render_template("index.html",balance=balance_list,num=(cash,mobycoin))
