from flask import Blueprint, request, jsonify
from app.models.subtask import SubTask
from app import db
from backend.app.models.task import Task

task_subtask_bp = Blueprint('task_subtask', __name__, url_prefix='/api/tasks/<int:task_id>/subtasks')
@task_subtask_bp.route('/', methods=['POST'])  # Only when it receives a POST request, the function can be triggered
def create_subtask(task_id):
    data = request.json  # To obtain the JSON data carried in the request body from frontend
    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    
    subtask = SubTask(  # Create an instance
        task_id=task_id,
        title=data['title'].strip(),
        description=data.get('description', ''),
        is_completed=False
    )
    db.session.add(subtask)  # Add the subtask object into database session
    db.session.commit()  # Commit the transaction to db
    return jsonify({
        'id': subtask.id,
        "title": subtask.title,
        "completed": subtask.is_completed
    }), 201  # Return a JSON response, and `subtask.id` is the primary key of automatic generation of db

@task_subtask_bp.route('/<int:subtask_id>', methods=['PUT'])
def update_subtask(task_id, subtask_id):
    subtask = SubTask.query.get_or_404(id=subtask_id, rask_id=task_id)
    data = request.json

    if 'title' in data:
        subtask.title = data['title'].strip()
    if 'completed' in data:
        subtask.is_completed = data['completed']

    db.session.commit() 
    return jsonify({
        "id": subtask.id,
        "title":subtask.title,
        "completed": subtask.is_completed
    }), 200

@task_subtask_bp.route('/batch', methods=['PUT'])
def batch_update_subtasks(task_id):
    try:
        data = request.get_json()
        
        # 校验主任务存在
        main_task = Task.query.get_or_404(task_id)
        
        # 处理更新和新建
        updated_ids = []
        new_subtasks = []
        
        # 处理所有子任务
        for sub_data in data.get('subtasks', []):
            if 'id' in sub_data:  # 更新现有
                subtask = SubTask.query.filter_by(id=sub_data['id'], task_id=task_id).first()
                if subtask:
                    subtask.title = sub_data.get('title', subtask.title)
                    updated_ids.append(subtask.id)
            else:  # 新建
                new_subtasks.append(SubTask(
                    task_id=task_id,
                    title=sub_data['title'],
                    is_completed=False
                ))
        
        # 提交变更
        db.session.add_all(new_subtasks)
        db.session.commit()
        
        # 返回完整子任务列表（包含新生成的ID）
        subtasks = SubTask.query.filter(
            (SubTask.id.in_(updated_ids)) | 
            (SubTask.task_id == task_id, SubTask.id.in_([s.id for s in new_subtasks]))
        ).all()
        
        return jsonify([{
            "id": s.id,
            "title": s.title,
            "completed": s.is_completed  # 与前端字段名对齐
        } for s in subtasks]), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@subtask_bp.route('/<int:subtask_id>', methods=['DELETE'])
def delete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return jsonify({'msg': 'Subtask has been deleted successfully.'})