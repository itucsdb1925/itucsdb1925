from flask import Flask
from flask_login import LoginManager
import views
from user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

app = Flask(__name__)
app.config.from_object("settings")
app.add_url_rule("/", view_func=views.sign_in,methods=['GET','POST'])
app.add_url_rule("/signup", view_func=views.sign_up,methods=['GET','POST'])
app.add_url_rule("/update", view_func=views.update,methods=['GET','POST'])
app.add_url_rule("/signedin", view_func=views.home_page,methods=['GET','POST'])
app.add_url_rule("/signout", view_func=views.sign_out, methods=['GET','POST'])
app.add_url_rule("/employees",view_func=views.employees_page, methods=['GET','POST'])
app.add_url_rule("/transactions",view_func=views.transaction_page, methods=['GET'])
app.add_url_rule("/request",view_func=views.request_page, methods=['GET','POST'])
lm.init_app(app)
lm.login_view = "sign_in"            

if __name__ == "__main__":
  app.run()
