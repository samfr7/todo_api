from flask import Blueprint , request, jsonify
from ..models import Todo
from ..extensions import db
from ..utils import token_required
from sqlalchemy import or_

todo_bp = Blueprint('todos', __name__)

@todo_bp.route('/todos', methods=['Post'])
@token_required
def create_todo(current_user):
    data = request.get_json()


    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({"message":'Title is required'}), 400

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


@todo_bp.route('/todos', methods=['GET'])
@token_required
def get_todos(current_user):

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status = request.args.get('status', None)
    sort_by = request.args.get('sort_by', None)
    order = request.args.get('order', 'asc')
    search = request.args.get('search', None)

    query = Todo.query.filter_by(user_id=current_user.id)

    if status:
        query = query.filter_by(status=status)
    
    valid_sort_columns = {
        'title': Todo.title,
        'status': Todo.status,
        'id': Todo.id
    }

    if sort_by:
        column = ""
        if sort_by in valid_sort_columns:
            column = valid_sort_columns[sort_by]
        
            if order:
                if order == 'asc':
                    query = query.order_by(column.asc())
                else:
                    query = query.order_by(column.desc())
        else:
            query = query.order_by(column)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Todo.title.ilike(search_term),
                Todo.description.ilike(search_term)
            )
        )


    todos = query.paginate(page=page, per_page=limit, error_out=False)
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

@todo_bp.route('/todos/<int:id>', methods=['GET'])
@token_required
def get_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first() 
    temp_todo = {}
    temp_todo['id'] = todo.id
    temp_todo['title'] = todo.title
    temp_todo['description'] = todo.description
    temp_todo['status'] = todo.status

    return jsonify({"data":temp_todo}), 200

@todo_bp.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
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

@todo_bp.route('/todos/<int:id>', methods=['DELETE'])
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
 