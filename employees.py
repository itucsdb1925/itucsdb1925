import psycopg2 as dbapi2
import names
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin

class Employees:
  def __init__(self, Id,Employer_name, Employee_name):
    self.id = Id
    self.employer_name = Employer_name
    self.employee_name = Employee_name
    