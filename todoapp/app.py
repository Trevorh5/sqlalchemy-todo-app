from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:54321@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)  
  completed = db.Column(db.Boolean, nullable=False, default=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id}, {self.description}>'

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:     
    description = request.get_json()['description']
    list_id = request.get_json()['list_id']
    newTodo = Todo(description=description, completed=False, list_id=list_id)
    db.session.add(newTodo)
    db.session.commit()
    body['description'] = newTodo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()

  if error: 
    abort(400)
  else:
    return jsonify(body) 


@app.route('/lists/create', methods=['POST'])
def create_list():
  error = False
  body = {}
  try:
    name = request.get_json()['name']
    newList = TodoList(name=name)
    db.session.add(newList)
    db.session.commit()
    body['name'] = newList.name
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally: 
    db.session.close()

  if error: 
    abort(400)
  else:
    return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try: 
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except: 
    db.session.rollback()
  finally: 
    db.session.close()

  return '', 200


@app.route('/lists/<list_id>/complete-list', methods=['POST'])
def complete_list(list_id):
  error = False

  try:
    print('listID', list_id)
    list = TodoList.query.get(list_id)

    for todo in list.todos:
      todo.completed = True
    
    db.session.commit()

  except:
    error = True
    db.session.rollback()
  finally: 
    db.session.close()

  if error: 
    abort(400)
  else: 
    return '', 200


@app.route('/todos/<todo_id>/delete-todo', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
  except:
    db.session.rollback()
  finally: 
    db.session.close()
  
  return jsonify({'success': True, 'id': todo_id})


@app.route('/lists/<list_id>/delete-list', methods=['DELETE'])
def delete_list(list_id):
  error = False
  
  try: 
    list = TodoList.query.get(list_id)

    for todo in list.todos:
      db.session.delete(todo)

    db.session.delete(list)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally: 
    db.session.close()

  if error:
    abort(400)
  else: 
    return '', 200


@app.route('/lists/<list_id>')
def get_todos_list(list_id):
  return render_template('index.html', 
  lists=TodoList.query.all(),
  active_list=TodoList.query.get(list_id),
  todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_todos_list', list_id=1))
