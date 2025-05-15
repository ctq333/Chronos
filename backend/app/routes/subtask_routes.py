from flask import Blueprint, request, jsonify
from app.models.subtask import SubTask
from app import db

subtask_bp = Blueprint('subtask', __name__, url_prefix='/api/subtask')  # Define a Blueprint object and automaticly add the '/api/subtask' prefix

@subtask_bp.route('/', methods=['POST'])  # Only when it receives a POST request, the function can be triggered
def create_subtask():
    data = request.json  # To obtain the JSON data carried in the request body from frontend
    subtask = SubTask(  # Create an instance
        main_task_id=data['main_task_id'],
        title=data['title'],
        description=data.get('description', ''),
        have_deadline=data.get('have_deadline', False),
        deadline=data.get('deadline'),
        is_completed=False
    )
    db.session.add(subtask)  # Add the subtask object into database session
    db.session.commit()  # Commit the transaction to db
    return jsonify({'msg': 'Subtask has been created successfully.', 'subtask_id': subtask.id})  # Return a JSON response, and `subtask.id` is the primary key of automatic generation of db

@subtask_bp.route('/<int:subtask_id>', methods=['PUT'])
def update_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    data = request.json
    subtask.title = data.get('title', subtask.title)
    subtask.description = data.get('description', subtask.description)
    subtask.have_deadline = data.get('have_deadline', subtask.have_deadline)
    subtask.deadline = data.get('deadline', subtask.deadline)
    db.session.commit() 
    return jsonify({'msg': 'Subtask has been updated successfully.'})

@subtask_bp.route('/<int:subtask_id>', methods=['DELETE'])
def delete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return jsonify({'msg': 'Subtask has been deleted successfully.'})