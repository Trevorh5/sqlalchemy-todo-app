from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# URI configuration = 'dialect://username:password@host:port/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:54321@localhost:5432/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Will default table name to lowercase version of class name, unless you specify a name with __tablename__ = 'tablename'
class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Person ID: {self.id}, Name: {self.name}>'

db.create_all()

@app.route('/')
def index():
  person = Person.query.first()
  return 'Hello ' + person.name 

if __name__ == '__main__':
  app.run()