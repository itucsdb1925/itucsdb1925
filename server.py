from flask import *
import psycopg2 as dbapi2
import names
from Classes import Balance,Database
app = Flask(__name__)

  
@app.route("/", methods=["POST","GET"])
def home_page():
  num1 = request.form.get("Cash")
  num2 = request.form.get("MobyCoin")
  given_name = request.form.get("Name")
  delete_id = request.form.get("id_of_balance")
  if(num1 and num2):
    num1=float(num1)
    num2=float(num2)
    print("hey john")
  dsn = """user='postgres' password='yattara'
  host='127.0.0.1' dbname='MobyCoin'"""
  database=Database(dsn)
  if(delete_id):
    balance_that_will_delete = database.get_balance(delete_id)
    database.delete_balance(balance_that_will_delete)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)