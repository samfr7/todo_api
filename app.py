from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'this_is_the_secret'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

    status = db.Column(
        db.Enum('open','in progress', 'completed', name='status_types'),
        default = 'open',
        nullable = False
    )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/register', methods=['Post'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # To check if the user already exists in the system

    user_exists = User.query.filter_by(username=username).first()

    if user_exists:
        return jsonify({"data":"username already exists"}), 400

    password_hash = generate_password_hash(password)

    user = User(username = username, password_hash = password_hash)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login_user'))

@app.route('/login', methods=["Post"])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username = username).first()

    if not user:
        return jsonify({"data":f"No username with {username} found"}), 401 

    if check_password_hash(user.password_hash, password=password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token":token}), 200
    else:
        return jsonify({"data":f"Wrong Password"}), 401

def token_required(f):
    # Need to learn why wraps
    # We need to use wrap as it copies the original functions data to this function makes it seem that this is the original function
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        token = token.split()[1]

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(id=data.get('user_id')).first()

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is Expired!"}), 401
            # Here we need to try to do the refresh token logic. we can do this later though
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is Invalid!"}), 401
        
        return f(user, *args, **kwargs)
    return decorated
        

@app.route('/todos', methods=['Post'])
@token_required
def create_todo(current_user):
    data = request.get_json()


    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({"message":'Title and Description, both are required'}), 400

    todo_data = {}
    try:
        todo = Todo(title=title, description=description, user_id= current_user.id)
        
        todo_data['id'] = todo.id
        todo_data['title'] = todo.title
        todo_data['description'] = todo.description


        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Internal Server Issue! Please try again later"}), 500
    
    return jsonify(todo_data), 201


@app.route('/todos', methods=['GET'])
@token_required
def get_todos(current_user):

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    todos = Todo.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=limit, error_out=False)
    # print(todos)
    # print(dir(todos))
    # print(todos.first)
    # print(todos.total)
    # print(todos.page)
    # print(todos.pages)
    # print(todos.has_next) #maybe refers page
    # print(todos.next())
    # print(todos.items)

    todos_list = []
    for todo in todos.items:
        temp_todo = {}
        temp_todo['id'] = todo.id
        temp_todo['title'] = todo.title
        temp_todo['description'] = todo.description
        temp_todo['status'] = todo.status
        todos_list.append(temp_todo)

    return jsonify({
        "data":todos_list,
        "page":page,
        "limit":limit,
        "total":todos.total
        }), 200

@app.route('/todos/<int:id>', methods=['GET'])
@token_required
def get_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first() 
    temp_todo = {}
    temp_todo['id'] = todo.id
    temp_todo['title'] = todo.title
    temp_todo['description'] = todo.description
    temp_todo['status'] = todo.status

    return jsonify({"data":temp_todo}), 200

@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
@token_required
def update_todo(current_user, id):
    try:
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    except Exception as e:
        return jsonify({"message":"Interna Server Error"}), 500

    if not todo:
        # in an assumption that if the id is not existing, then it will return this error
        return jsonify({"message":"Forbidden"}), 403
    
    data = request.get_json()

    if not data:
        return jsonify({"message":"Please provide a valid json"}), 400
    
    

    try:
        todo.title = data.get('title',todo.title)
        todo.description = data.get('description',todo.description)
        todo.status = data.get('status',todo.status)

        # db.session.add(todo)
        # The above line is not required as the todo is already an object of the ToDo Model of table.
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Internal Server Issue! Please try again later"}), 500



    return jsonify({"message":"Successfully updated the todo"}), 200

@app.route('/todos/<int:id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, id):
    try:
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    except Exception as e:
        return jsonify({"message":"Interna Server Error"}), 500

    if not todo:
        # in an assumption that if the id is not existing, then it will return this error
        return jsonify({"message":"The mentioned id is invalid or deleted. Please select a valid todo"}), 400  
    

    try:
        todo.status = 'completed'

        # Or we can perform a delete operation as well, not a issue. Depends on the requirement.
        # db.session.delete(todo)

        # db.session.add(todo)
        # The above line is not required as the todo is already an object of the ToDo Model of table.
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Internal Server Issue! Please try again later"}), 500



    return '', 204
        

if __name__ == "__main__":
    app.run(debug=True)