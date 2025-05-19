from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, SubTask
from datetime import datetime, date
from app.routes.auth_routes import login_required  # 假设你的登录验证装饰器在这里

bp = Blueprint("task", __name__, url_prefix="/task")

@bp.route('/create', methods=['POST'])
@login_required()
def create_task(current_user):
    """
    创建事项接口，要求登录
    """
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求体不能为空"}), 400

    # 字段校验
    title = data.get("title", "").strip()
    plan_date = data.get("planDate")
    due_date = data.get("dueDate")
    priority = data.get("priority", 2)
    notes = data.get("notes", "")
    tags = data.get("tags", [])
    subtasks = data.get("subtasks", [])
    
    if not title or not plan_date or not due_date:
        return jsonify({"code": 400, "message": "标题、计划处理日期、截止日期为必填项"}), 400

    try:
        # 字段转换
        plan_date_obj = datetime.strptime(plan_date, "%Y-%m-%d").date()
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        tag_str = ",".join(tags) if tags else None

        # 创建 Task 实例
        task = Task(
            user_id=current_user.id,
            title=title,
            plan_date=plan_date_obj,
            due_date=due_date_obj,
            priority=priority,
            notes=notes,
            status=0,  # 0=未开始, 1=进行中, 2=已完成，可以按你的枚举来
            tag=tag_str,
            postpone_count=0,
            progress=0,
        )

        # 处理子任务
        for sub in subtasks:
            sub_title = sub.get("title", "").strip()
            if not sub_title:
                continue
            subtask = SubTask(
                title=sub_title,
                completed=sub.get("completed", False)
            )
            task.subtasks.append(subtask)

        db.session.add(task)
        db.session.commit()

        # 返回成功，附带新事项id等
        return jsonify({
            "code": 201,
            "message": "事项创建成功",
            "data": {
                "id": task.id,
                "title": task.title
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"服务器错误: {str(e)}"}), 500
    
@bp.route('/list', methods=['GET'])
@login_required()
def get_task_list(current_user):
    """
    获取当前登录用户的所有事项及其子任务
    """
    tasks = (
        Task.query
        .filter_by(user_id=current_user.id)
        .order_by(Task.status.asc(), Task.due_date.asc(), Task.plan_date.asc())
        .all()
    )

    def serialize_task(task):
        return {
            "id": task.id,
            "title": task.title,
            "planDate": task.plan_date.strftime("%Y-%m-%d") if task.plan_date else "",
            "dueDate": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "priority": task.priority,
            "tags": task.tag.split(",") if task.tag else [],
            "postponeCount": task.postpone_count,
            "notes": task.notes,
            "subtasks": [
                {
                    "id": sub.id,
                    "title": sub.title,
                    "completed": bool(sub.completed)
                } for sub in task.subtasks
            ],
            "progress": task.progress,
            "status": (
                "completed" if task.status == 2
                else "in-progress" if task.status == 1
                else "not-started"
            )
        }

    return jsonify({
        "code": 200,
        "data": {
            "tasks": [serialize_task(task) for task in tasks]
        }
    })


@bp.route('/home', methods=['GET'])
@login_required()
def get_task_home(current_user):
    """
    获取当前登录用户当日的未完成事项
    """
    tasks = (
        Task.query
        .filter_by(user_id=current_user.id)
        .filter(Task.plan_date<=date.today(), Task.due_date>=date.today())
        .filter(Task.progress!=100)
        .order_by(Task.status.asc(), Task.due_date.asc(), Task.plan_date.asc())
        .all()
    )

    def serialize_task(task):
        return {
            "id": task.id,
            "title": task.title,
            "planDate": task.plan_date.strftime("%Y-%m-%d") if task.plan_date else "",
            "dueDate": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "priority": task.priority,
            "tags": task.tag.split(",") if task.tag else [],
            "postponeCount": task.postpone_count,
            "notes": task.notes,
            "subtasks": [
                {
                    "id": sub.id,
                    "title": sub.title,
                    "completed": bool(sub.completed)
                } for sub in task.subtasks
            ],
            "progress": task.progress,
            "status": (
                "completed" if task.status == 2
                else "in-progress" if task.status == 1
                else "not-started"
            )
        }

    return jsonify({
        "code": 200,
        "data": {
            "tasks": [serialize_task(task) for task in tasks]
        }
    })


@bp.route('/<int:task_id>/toggle_complete', methods=['POST'])
@login_required()
def toggle_task_complete(current_user, task_id):
    """
    切换事项完成状态
    """
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    if task.status == 2:
        # 已完成->改为进行中
        task.status = 1
        task.progress = 0
        msg = '事项已标记为未完成'
    else:
        # 未完成->改为完成
        task.status = 2
        task.progress = 100
        msg = '事项已标记为完成'

    db.session.commit()
    return jsonify({'code': 200, 'message': msg, 'data': {
        'id': task.id,
        'status': 'completed' if task.status == 2 else 'in-progress',
        'progress': task.progress
    }})

@bp.route('/<int:task_id>/update', methods=['POST'])
@login_required()
def update_task(current_user, task_id):
    """
    编辑事项及其子任务
    """
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求体不能为空'}), 400

    try:
        title = data.get("title", "").strip()
        plan_date = data.get("planDate")
        due_date = data.get("dueDate")
        priority = data.get("priority", 2)
        notes = data.get("notes", "")
        tags = data.get("tags", [])
        subtasks = data.get("subtasks", [])

        if not title or not plan_date or not due_date:
            return jsonify({"code": 400, "message": "标题、计划处理日期、截止日期为必填项"}), 400

        # 更新主任务
        task.title = title
        task.plan_date = datetime.strptime(plan_date, "%Y-%m-%d").date()
        task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task.priority = priority
        task.notes = notes
        task.tag = ",".join(tags) if tags else None

        old_subtasks = {sub.id: sub for sub in task.subtasks}
        incoming_ids = set()

        for sub in subtasks:
            sub_id = sub.get("id")
            sub_title = sub.get("title", "").strip()
            if not sub_title:
                continue
            if sub_id:  # 已有子任务，更新
                subtask = old_subtasks.get(sub_id)
                if subtask:
                    subtask.title = sub_title
                    subtask.completed = bool(sub.get("completed", False))
                incoming_ids.add(sub_id)
            else:  # 新增子任务
                # 这里必须加 parent_task_id
                new_sub = SubTask(
                    parent_task_id=task.id,
                    title=sub_title,
                    completed=bool(sub.get("completed", False))
                )
                db.session.add(new_sub)

        # 删除被移除的子任务
        for old_sub in task.subtasks:
            if old_sub.id not in incoming_ids:
                db.session.delete(old_sub)

        db.session.commit()
        return jsonify({'code': 200, 'message': '事项已更新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500
    
@bp.route('/<int:task_id>/delete', methods=['DELETE'])
@login_required()
def delete_task(current_user, task_id):
    """
    删除指定事项及其所有子任务
    """
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'code': 200, 'message': '事项已删除'})


@bp.route('/<int:task_id>/progress', methods=['POST'])
@login_required()
def update_task_progress(current_user, task_id):
    """
    更新事项进度
    """
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    data = request.get_json()
    progress = data.get('progress')
    if progress is None or not (0 <= progress <= 100):
        return jsonify({'code': 400, 'message': '进度必须在0到100之间'}), 400

    task.progress = int(progress)
    # 如果进度100，自动标记为已完成
    if task.progress == 100:
        task.status = 2  # completed
    elif task.status == 2 and task.progress < 100:
        task.status = 1  # in-progress

    db.session.commit()
    return jsonify({'code': 200, 'message': '进度已更新', 'data': {'progress': task.progress, 'status': task.status}})

@bp.route('/<int:task_id>/postpone', methods=['POST'])
@login_required()
def postpone_task(current_user, task_id):
    data = request.get_json()
    new_plan_date_str = data.get('newPlanDate')
    if not new_plan_date_str:
        return jsonify({'code': 400, 'message': '新计划日期不能为空'}), 400

    try:
        new_plan_date = datetime.strptime(new_plan_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'code': 400, 'message': '日期格式错误'}), 400

    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    task.plan_date = new_plan_date
    task.postpone_count = (task.postpone_count or 0) + 1

    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '事项已推迟', 'data': {
            'planDate': new_plan_date_str,
            'postponeCount': task.postpone_count
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500


@bp.route('/subtask/<int:subtask_id>/toggle_completed', methods=['POST'])
@login_required()
def toggle_subtask_completed(current_user, subtask_id):
    """
    切换子任务完成状态
    """
    subtask = SubTask.query.get(subtask_id)
    if not subtask:
        return jsonify({'code': 404, 'message': '子任务不存在'}), 404

    # 校验子任务是否属于当前用户
    parent_task = Task.query.filter_by(id=subtask.parent_task_id, user_id=current_user.id).first()
    if not parent_task:
        return jsonify({'code': 403, 'message': '无权限操作该子任务'}), 403

    subtask.completed = 0 if subtask.completed else 1
    db.session.commit()
    return jsonify({'code': 200, 'message': '子任务状态已切换', 'data': {'completed': bool(subtask.completed)}})

@bp.route('/<int:task_id>/add_subtask', methods=['POST'])
@login_required()
def add_subtask(current_user, task_id):
    """
    向指定事项添加子任务
    """
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'code': 404, 'message': '事项不存在或无权限'}), 404

    data = request.get_json()
    title = data.get('title', '').strip()
    completed = bool(data.get('completed', False))
    if not title:
        return jsonify({'code': 400, 'message': '子任务标题不能为空'}), 400

    subtask = SubTask(
        parent_task_id=task.id,
        title=title,
        completed=completed
    )
    db.session.add(subtask)
    db.session.commit()

    # 返回新子任务的真实id
    return jsonify({
        'code': 201,
        'message': '子任务已添加',
        'data': {
            'id': subtask.id,
            'title': subtask.title,
            'completed': subtask.completed
        }
    }), 201