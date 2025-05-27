from flask import Blueprint, jsonify, request, current_app
from app.models import Schedule, ScheduleInvitation, User
from datetime import datetime, timedelta
from app.routes.auth_routes import login_required

bp = Blueprint("invitation", __name__, url_prefix="/invitation")

@bp.route("/fetch", methods=["GET"])
@login_required()
def get_invitation_list(user):
    db = current_app.extensions["sqlalchemy"]
    query = (db.session.query(ScheduleInvitation, Schedule, User)
            .join(Schedule, ScheduleInvitation.schedule_id == Schedule.id)
            .join(User, ScheduleInvitation.sender_id == User.id)
            .filter(ScheduleInvitation.receiver_id == user.id, 
                    ScheduleInvitation.status == 0)
            .order_by(ScheduleInvitation.created_at))

    results = query.all()
    data = []
    for invitation, schedule, sender in results:
        data.append({
            "id": invitation.id,
            "name": schedule.title,
            "startTime": schedule.start_time.isoformat(),
            "endTime": schedule.end_time.isoformat(),
            "sender": sender.username,
            "location": schedule.location
        })
    return jsonify({"success": True, "data": data})


@bp.route("/accept", methods=["POST"])
@login_required()
def invitation_accept(user):
    db = current_app.extensions["sqlalchemy"]
    try:
        data = request.get_json()
        invitation_id = data['id']
        invitation = ScheduleInvitation.query.get(invitation_id)
        if not invitation:
            return jsonify({"code": 404, "message": "邀请记录不存在"}), 404
        invitation.status = 1
        schedule = Schedule.query.get(invitation.schedule_id)
        schedule.user_id = invitation.receiver_id
        db.session.add(schedule)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "日程接收成功",
            "data": {
                "id": invitation.id,
                "schedule_id": invitation.schedule_id,
                "status": invitation.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"服务器错误: {str(e)}"}), 500
    

@bp.route("/reject", methods=["POST"])
@login_required()
def invitation_reject(user):
    db = current_app.extensions["sqlalchemy"]
    try:
        data = request.get_json()
        invitation_id = data['id']
        invitation = ScheduleInvitation.query.get(invitation_id)
        if not invitation:
            return jsonify({"code": 404, "message": "邀请记录不存在"}), 404
        invitation.status = 2
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "日程拒绝成功",
            "data": {
                "id": invitation.id,
                "schedule_id": invitation.schedule_id,
                "status": invitation.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"服务器错误: {str(e)}"}), 500