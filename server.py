from flask import *

import views




def create_app():
  app = Flask(__name__)
  app.config.from_object("settings")
  app.add_url_rule("/signin", view_func=views.sign_page,methods=['GET','POST'])
  app.add_url_rule("/signup", view_func=views.sign_up,methods=['GET','POST'])
  app.add_url_rule("/update", view_func=views.update,methods=['GET','POST'])
  app.add_url_rule("/signedin", view_func=views.home_page,methods=['GET','POST'])
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)
