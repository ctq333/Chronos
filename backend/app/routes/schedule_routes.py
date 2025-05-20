from flask import Blueprint, jsonify, request, current_app
from app.models import Schedule, ScheduleInvitation, User
from datetime import datetime, timedelta
from app.routes.auth_routes import login_required

bp = Blueprint("schedule", __name__, url_prefix="/schedule")

@bp.route("/fetch", methods=["GET"])
@login_required()
def get_schedule_list(user):
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = Schedule.query.filter_by(user_id=user.id)
    if start_date and end_date:
        try:
            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)
            query = query.filter(
                Schedule.start_time >= start_datetime,
                Schedule.start_time < end_datetime
            )
        except ValueError:
            return jsonify({"code": 400, "message": "日期格式错误"})
    schedules = query.order_by(Schedule.start_time).all()

    data = []
    for sch in schedules:
        data.append({
            "id": sch.id,
            "title": sch.title,
            "description": sch.description,
            "start": sch.start_time.isoformat()[:16],  # 'YYYY-MM-DDTHH:MM'
            "end": sch.end_time.isoformat()[:16] if sch.end_time else "",
            "location": sch.location,
            "link": sch.link
        })
    return jsonify({"code": 200, "data": data, "message": "日程获取成功"})


@bp.route("/create", methods=["POST"])
@login_required()
def create_schedule(user):
    db = current_app.extensions["sqlalchemy"]
    data = request.get_json()
    try:
        start_time = datetime.fromisoformat(data['start'])
        end_time = datetime.fromisoformat(data['end'])
    except ValueError:
        return jsonify({"code": 400, "message": "日期格式错误"})
 
    schedule = Schedule(
        user_id=user.id,
        title=data['title'],
        start_time=start_time,
        end_time=end_time,
        location=data.get('location'),
        link=data.get('link'),
        description=data.get('description'),
    )
 
    try:
        db.session.add(schedule)
        db.session.commit()
        return jsonify({
            "code": 200, 
            "data": {
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "start": schedule.start_time.isoformat()[:16],
                "end": schedule.end_time.isoformat()[:16],
                "location": schedule.location,
                "link": schedule.link
            },
            "message": "日程创建成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "日程创建失败"})
 
@bp.route("/update/<int:schedule_id>", methods=["POST"])
@login_required()
def update_schedule(user, schedule_id):  
    db = current_app.extensions["sqlalchemy"]
    data = request.get_json()
    try:
        start_time = datetime.fromisoformat(data['start'])
        end_time = datetime.fromisoformat(data['end'])
    except ValueError:
        return jsonify({"code": 400, "message": "日期格式错误"})
 
    schedule = Schedule.query.filter_by(id=schedule_id, user_id=user.id).first()
    if not schedule:
        return jsonify({"code": 404, "message": "未找到该日程"})
 
    schedule.title = data['title']
    schedule.description = data.get('description')
    schedule.start_time = start_time
    schedule.end_time = end_time
    schedule.location = data.get('location')
    schedule.link = data.get('link')
 
    try:
        db.session.commit()
        return jsonify({
            "code": 200, 
            "data": {
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "start": schedule.start_time.isoformat()[:16],
                "end": schedule.end_time.isoformat()[:16],
                "location": schedule.location,
                "link": schedule.link
            },
            "message": "日程更新成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "更新日程失败"})
    

@bp.route("/delete/<int:schedule_id>", methods=["DELETE"])
@login_required()
def delete_schedule(user, schedule_id):
    db = current_app.extensions["sqlalchemy"]
    schedule = Schedule.query.get_or_404(schedule_id)

    try:
        db.session.delete(schedule)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"code":409, "message": "日程删除失败"})

    return jsonify({"code":200, "message": "日程删除成功"})


@bp.route("/invite", methods=["POST"])
@login_required()
def invite(user):
    db = current_app.extensions["sqlalchemy"]
    data = request.get_json()
    schedule_id = data['scheduleId']
    receiver_name = data['receiver']

    receiver = db.session.query(User).filter_by(username=receiver_name).first()
    if not receiver:
        return jsonify({"code": 409, "message": "未找到该用户"})

    invitation = ScheduleInvitation(
        schedule_id = schedule_id,
        sender_id = user.id,
        receiver_id = receiver.id,
        created_at = datetime.utcnow(),
        status = 0
    )
 
    try:
        db.session.add(invitation)
        db.session.commit()
        return jsonify({
            "code": 200, 
            "data": {
            },
            "message": "邀请发送成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "邀请发送失败"})
    

@bp.route('/batch_create', methods=['POST'])
@login_required()
def batch_create(current_user):
    db = current_app.extensions["sqlalchemy"]
    data = request.get_json()
    schedules = data.get("schedules", [])
    created = []
    for s in schedules:
        title = s.get("title", "").strip()
        description = s.get("description", "")
        start = s.get("start")
        end = s.get("end")
        location = s.get("location", "")
        link = s.get("link", "")

        # 时间格式校验
        if not title or not start or not end:
            continue

        start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        end_dt = datetime.strptime(end, "%Y-%m-%dT%H:%M")

        schedule = Schedule(
            user_id=current_user.id,
            title=title,
            description=description,
            start_time=start_dt,
            end_time=end_dt,
            location=location,
            link=link
        )
        db.session.add(schedule)
        db.session.flush()
        created.append({
            "id": schedule.id,
            "title": schedule.title,
            "start": start,
            "end": end,
            "location": schedule.location,
            "link": schedule.link,
            "description": schedule.description,
        })
    db.session.commit()
    return jsonify({"code": 201, "data": created, "message": "批量日程创建成功"})
