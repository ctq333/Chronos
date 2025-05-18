from flask import Blueprint, request, jsonify
from app.models.subtask import SubTask
from app import db
from app.models.task import Task

task_subtask_bp = Blueprint('task_subtask', __name__, url_prefix='/api/tasks/<int:task_id>/subtasks')
@task_subtask_bp.route('/', methods=['POST'])  # Only when it receives a POST request, the function can be triggered
def create_subtask(task_id):
    data = request.json  # To obtain the JSON data carried in the request body from frontend
    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    
    subtask = SubTask(  # Create an instance
        parent_task_id=task_id,
        title=data['title'].strip(),
        completed=False
    )
    db.session.add(subtask)  # Add the subtask object into database session
    db.session.commit()  # Commit the transaction to db
    return jsonify({
        'id': subtask.id,
        "title": subtask.title,
        "completed": subtask.completed
    }), 201  # Return a JSON response, and `subtask.id` is the primary key of automatic generation of db

@task_subtask_bp.route('/<int:subtask_id>', methods=['PUT'])
def update_subtask(task_id, subtask_id):
    subtask = SubTask.query.filter_by(id=subtask_id, task_id=task_id).first_or_404()
    data = request.json

    if 'title' in data:
        subtask.title = data['title'].strip()
    if 'completed' in data:
        subtask.completed = data['completed']

    db.session.commit() 
    return jsonify({
        "id": subtask.id,
        "title":subtask.title,
        "completed": subtask.completed
    }), 200

@task_subtask_bp.route('/batch', methods=['PUT'])
def batch_update_subtasks(task_id):
    try:
        data = request.get_json()
        
        # Check if parent task exists
        parent_task = Task.query.get_or_404(task_id)
        
        updated_ids = []
        new_subtasks = []
        
        for sub_data in data.get('subtasks', []):
            if 'id' in sub_data:  # Update
                subtask = SubTask.query.filter_by(id=sub_data['id'], task_id=task_id).first()
                if subtask:
                    subtask.title = sub_data.get('title', subtask.title)
                    updated_ids.append(subtask.id)
            else:  # Create a new subtask
                new_subtasks.append(SubTask(
                    task_id=task_id,
                    title=sub_data['title'],
                    completed=False
                ))
        
        # Commit the change
        db.session.add_all(new_subtasks)
        db.session.commit()
        
        # Return completed subtask list
        subtasks = SubTask.query.filter(
            (SubTask.id.in_(updated_ids)) | 
            (SubTask.task_id == task_id, SubTask.id.in_([s.id for s in new_subtasks]))
        ).all()
        
        return jsonify([{
            "id": s.id,
            "title": s.title,
            "completed": s.completed
        } for s in subtasks]), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@task_subtask_bp.route('/<int:subtask_id>', methods=['DELETE'])
def delete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return jsonify({'msg': 'Subtask has been deleted successfully.'})

@task_subtask_bp.route('/test', methods=['POST'])
def test_subtask_route(task_id):
    return "Subtask route works!"