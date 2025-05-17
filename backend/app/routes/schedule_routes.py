from flask import Blueprint, jsonify, request
from app.models import Schedule

bp = Blueprint("schedule", __name__, url_prefix="/schedule")

@bp.route("/list", methods=["GET"])
def get_schedule_list():
    """
    获取指定用户的所有日程（暂不做token校验）
    需要传入 GET 参数：user_id
    """
    user_id = request.args.get("user_id", type=int)
    token = request.headers.get("Authorization", "")  # 伪token，暂不校验

    if not user_id:
        return jsonify({"success": False, "msg": "缺少 user_id"}), 400

    schedules = Schedule.query.filter_by(user_id=user_id).order_by(Schedule.start_time.desc()).all()
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
    return jsonify({"success": True, "data": data})