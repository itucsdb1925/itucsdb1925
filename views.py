from flask import Flask,render_template,request,redirect,flash,url_for
import psycopg2 as dbapi2
from balance import Balance
from user import User,get_user
from database import Database
from employees import Employees
from transaction import Cash_Transactions,MobyCoin_Transactions
from request import MobyCoin_Requests,Cash_Requests
from forms import SigninForm
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
import os
dsn =  os.getenv("DATABASE_URL")

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
    database.create_employees()
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
  database.create_employees()
  if(username and password):
    user=User(username,password)
    database.add_user(user)
    balance=Balance(0,username)
    database.add_balance(balance)
    next_page = request.args.get("next", url_for("home_page"))
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

@login_required
def transaction_page():
  user_id = current_user.get_id()
  database=Database(dsn)
  cash_transactions = database.get_cash_transactions(user_id)
  mobyCoin_transactions = database.get_mobyCoin_transactions(user_id)
  print(cash_transactions)
  return render_template("transactions.html",cash_transactions=cash_transactions,mobyCoin_transactions=mobyCoin_transactions)

@login_required
def request_page():
  user_id = current_user.get_id()
  user = get_user(user_id)

  sender_name_cash = request.form.get("SenderNameCash")
  description_cash = request.form.get("DescriptionCash")
  cash = request.form.get("Cash")

  sender_name_mobyCoin = request.form.get("SenderNameMobyCoin")
  description_mobyCoin = request.form.get("DescriptionMobyCoin")
  mobyCoin = request.form.get("MobyCoin")

  accept_request_id_mobyCoin = request.form.get("accept_request_id_mobyCoin")
  decline_request_id_mobyCoin = request.form.get("decline_request_id_mobyCoin")
  accept_request_id_cash = request.form.get("accept_request_id_cash")
  decline_request_id_cash = request.form.get("decline_request_id_cash")
  database=Database(dsn)
  database.create_cash_requests();
  database.create_mobyCoin_requests();
  


  if(cash):
    cash_request=Cash_Requests(0,sender_name_cash,user_id,cash,description_cash)
    database.create_cash_requests()
    database.add_cash_request(cash_request)
  if(mobyCoin):
    mobyCoin_request=MobyCoin_Requests(0,sender_name_mobyCoin,user_id,mobyCoin,description_mobyCoin)
    database.create_mobyCoin_requests()
    database.add_mobyCoin_request(mobyCoin_request)
  if(accept_request_id_cash):
    cash_request = database.get_cash_request(accept_request_id_cash)
    balance_src = database.get_balance(cash_request.sender_name)
    balance_dst = database.get_balance(cash_request.receiver_name)
    requested_cash = cash_request.cash
    if(database.transfer_between_users_cash(balance_src,balance_dst,requested_cash)):
      database.create_cash_transactions()
      cash_transaction = Cash_Transactions(0,balance_src.user_name,balance_dst.user_name,requested_cash)
      database.add_cash_transaction(cash_transaction)
      database.delete_cash_request(accept_request_id_cash)
  if(decline_request_id_cash):
    database.delete_cash_request(decline_request_id_cash)

  if(accept_request_id_mobyCoin):
    mobyCoin_request = database.get_mobyCoin_request(accept_request_id_mobyCoin)
    balance_src = database.get_balance(mobyCoin_request.sender_name)
    balance_dst = database.get_balance(mobyCoin_request.receiver_name)
    requested_mobyCoin = mobyCoin_request.mobyCoin
    if(database.transfer_between_users_mobycoin(balance_src,balance_dst,requested_mobyCoin)):
      database.create_mobyCoin_transactions()
      mobyCoin_transaction = MobyCoin_Transactions(0,balance_src.user_name,balance_dst.user_name,requested_mobyCoin)
      database.add_mobyCoin_transaction(mobyCoin_transaction)
      database.delete_mobyCoin_request(accept_request_id_mobyCoin)
  if(decline_request_id_mobyCoin):
    database.delete_mobyCoin_request(decline_request_id_mobyCoin)

  past_cash_requests=database.get_cash_requests(user_id)
  past_mobyCoin_requests=database.get_mobyCoin_requests(user_id)
  return render_template("request.html",past_cash_requests=past_cash_requests,past_mobyCoin_requests=past_mobyCoin_requests)

@login_required
def employees_page():
  user_id = current_user.get_id()
  user = get_user(user_id)

  employer_name = user_id
  employee_name_to_add = request.form.get("EmployeeName")
  pay_salary_cash = request.form.get("PaySalaryCash")
  pay_salary_mobyCoin = request.form.get("PaySalaryMobyCoin")
  database=Database(dsn)
  all_employees = database.get_employee(employer_name)
  if(pay_salary_cash):
    balance_employer = database.get_balance(employer_name)
    if(balance_employer.cash >= (float(pay_salary_cash)*len(all_employees))):
      for i in range(len(all_employees)):
        balance_employee=database.get_balance(all_employees[i])
        database.salary_payment_cash(balance_employer,balance_employee,float(pay_salary_cash))
  if(pay_salary_mobyCoin):
    balance_employer = database.get_balance(employer_name)
    if(balance_employer.mobyCoin >= (float(pay_salary_mobyCoin)*len(all_employees))):
      for i in range(len(all_employees)):
        balance_employee=database.get_balance(all_employees[i])
        database.salary_payment_mobyCoin(balance_employer,balance_employee,float(pay_salary_mobyCoin))
  if(employer_name and employee_name_to_add):
    employees=Employees(0,employer_name,employee_name_to_add)
    database.add_employee(employees)

  delete_employee_id = request.form.get("delete_employee_id")

  if(delete_employee_id):
    database.delete_employee(delete_employee_id)


  connection = dbapi2.connect(dsn)
  cursor = connection.cursor()
  sql_command="SELECT * FROM EMPLOYEES WHERE (EMPLOYER_NAME = %(employer_name)s)"
  cursor.execute(sql_command,{'employer_name':employer_name})
  fetched = cursor.fetchall()
  employees_list = []
  for i in fetched:
    employees_list.append(Employees(i[0],i[1],i[2]))


  #statement = """INSERT INTO PERSON (
  #NAME) VALUES (%(name_person)s)"""
  #cursor.execute(statement,{'name_person':names.get_full_name()})
  connection.commit()
  cursor.close()
  connection.close()

  return render_template("employees.html",employees_list=employees_list)

#@app.route("/signedin", methods=["POST","GET"])
@login_required
def home_page():
  user_id = current_user.get_id()
  user = get_user(user_id)
  cash_to_mobyCoin = request.form.get("CashtoMobyCoin")
  mobyCoin_to_cash = request.form.get("MobyCointoCash")

  transfer_name_cash = request.form.get("TransferNameCash")
  transfer_amount_cash = request.form.get("TransferAmountCash")

  transfer_name_mobyCoin = request.form.get("TransferNameMobyCoin")
  transfer_amount_mobyCoin = request.form.get("TransferAmountMobyCoin")

  add_cash = request.form.get("BuyCash")

  #given_name = request.form.get("Name")
  delete_id = request.form.get("id_to_delete")
  update_id = request.form.get("id_to_update")
  database=Database(dsn)
  database.create_balance()
  
  if(add_cash):
    add_cash = float(add_cash)
    if(user):
      balance=database.get_balance(user_id)
      database.buy_cash(balance,add_cash)
  if(cash_to_mobyCoin):
    cash_to_mobyCoin=float(cash_to_mobyCoin)
    if(user):
      balance=database.get_balance(user_id)
      database.buy_mobycoin(balance,cash_to_mobyCoin)
  if(mobyCoin_to_cash):
    mobyCoin_to_cash=float(mobyCoin_to_cash)
    if(user):
      balance=database.get_balance(user_id)
      database.sell_mobycoin(balance,mobyCoin_to_cash)

  if(transfer_name_cash):
    transfer_amount_cash=float(transfer_amount_cash)
    if(user):
      balance_src=database.get_balance(user_id)
      balance_dst=database.get_balance(transfer_name_cash)
      database.transfer_between_users_cash(balance_src,balance_dst,transfer_amount_cash)
      database.create_cash_transactions()
      cash_transaction = Cash_Transactions(0,balance_src.user_name,balance_dst.user_name,transfer_amount_cash)
      database.add_cash_transaction(cash_transaction)

  if(transfer_name_mobyCoin):
    transfer_amount_mobyCoin=float(transfer_amount_mobyCoin)
    if(user):
      balance_src=database.get_balance(user_id)
      balance_dst=database.get_balance(transfer_name_mobyCoin)
      database.transfer_between_users_mobycoin(balance_src,balance_dst,transfer_amount_mobyCoin)
      database.create_mobyCoin_transactions()
      mobyCoin_transaction = MobyCoin_Transactions(0,balance_src.user_name,balance_dst.user_name,transfer_amount_mobyCoin)
      database.add_mobyCoin_transaction(mobyCoin_transaction)

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
  return render_template("index.html",balance=balance_list)
