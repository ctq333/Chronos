import json
from flask import Blueprint, jsonify, request
from datetime import datetime, date, timedelta
from sqlalchemy import extract
from app import db
from app.models.schedule import Schedule
from app.models.task import Task
from app.models.monthly_report import MonthlyReport
from app.routes.auth_routes import login_required
from app.services.genai_service import generate_content
from app.utils import extract_json_from_string
from datetime import datetime, timedelta
from sqlalchemy import and_
from app import db
from app.models import Task, Schedule, WeeklyReport
from app.routes.auth_routes import login_required
import json

bp = Blueprint("llm", __name__, url_prefix="/llm")

MONTHLY_REPORT_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with json content contains tasks and schedules, which is schedules user engaged and tasks user completed last month. You need to summraize what the user done last month, like what this user have accomplished, what this user have postponed, or anything relavent, then write a monthly report. The report should be write with plain text in multiple paragraph, rather than markdown format. The human language you used to fill into JSON should be the language you recognized in provided json, if multiple language are used in provided json, choose the language that is used most.
JSON Schema:
[
    {
        "content": str  # The content of the monthly report
    }
]
also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the json data contains schedule and task:
"""



TASK_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with a paragraph, which can contain multiple tasks, each task can include a task heading, plan date, due date, priority, tags, notes. You need to recognize those things in the paraghaph accurately, without any mistake and return them in JSON. JSON fields can be left empty if not recognized, except for planDate and dueTime, which should be filled with the recognized date. You can choose an proper plan date if no plan date is provided, and set due date to one day later if no due date is provided. The language you used to fill into JSON should be the language you recognized in the text. 

JSON Schema:
[
    {
        "heading": str,
        "planDate": str,    # Use "yyyy-mm-dd" format; if no plan date is recognized, choose a proper plan date. If no date is recognized, use today's date.
        "dueDate": str,      # Use "yyyy-mm-dd" format; if no due date is found, set it to one day later.
        "priority": int,     # 0=low, 1=medium, 2=high, 3=urgent
        "tags": str,   # List of recognized tags in the text, use "," to split them.
        "notes": str         # Key points for one single task summarized as a string.
    },
    {
        "heading": str,
        "planDate": str,    # Use "yyyy-mm-dd" format; if no plan date is recognized, choose a proper plan date. If no date is recognized, use today's date.
        "dueDate": str,      # Use "yyyy-mm-dd" format; if no due date is found, set it to one day later.
        "priority": int,     # 0=low, 1=medium, 2=high, 3=urgent
        "tags": str,   # List of recognized tags in the text, use "," to split them.
        "notes": str         # Key points for one single task summarized as a string.
    },
    ...
]

also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the paragraph:
"""

WEEKLY_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with json content contains tasks and schedules, which is schedules user engaged and tasks user completed last week. You need to summraize what the user done last week, like what this user have accomplished, what this user have postponed, or anything relavent, then write a weekly report. The report should be write with plain text in multiple paragraph, rather than markdown format. The human language you used to fill into JSON should be the language you recognized in provided json, if multiple language are used in provided json, choose the language that is used most.
JSON Schema:
[
    {
        "content": str,  # The content of the weekly report
    }
]
also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the json data comtains schedule and task:
"""

SUBTASK_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with json content contains one task user needs to complete. Your task is that plan one or more subtasks based on what user provided in json. The human language you used to fill into JSON should be the language you recognized in provided json.
JSON Schema:
[
    {
        "title": str,  # The heading of the subtask
    },
    {
        "title": str,  # The heading of the subtask
    },
]
also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the json data comtains one task:
"""


def get_month_start_end(dt=None):
    """返回本月第一天和最后一天"""
    if dt is None:
        dt = date.today()
    start = dt.replace(day=1)
    # 下月1日-1天
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1, day=1)
    else:
        next_month = start.replace(month=start.month + 1, day=1)
    end = next_month - timedelta(days=1)
    return start, end
  
def get_week_range(date=None):
    # 返回本周一到本周日日期
    if not date:
        date = datetime.now().date()
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end

# Create a blueprint for the main routes
bp = Blueprint("llm", __name__, url_prefix="/llm")

@bp.route("/createSchedule", methods=["POST"])
def create_schedule():
    try:
        # Get input paragraph
        input_data = request.json
        paragraph = input_data.get("paragraph", "")


@bp.route("/generateMonthlyReport", methods=["POST"])
@login_required()
def generate_monthly_report(user):
    today = date.today()
    month_start, month_end = get_month_start_end(today)

    # 查询本月所有Tasks（plan_date在本月）
    tasks = Task.query.filter(
        Task.user_id == user.id,
        extract('year', Task.plan_date) == today.year,
        extract('month', Task.plan_date) == today.month
    ).all()
    # 查询本月所有Schedules（start_time在本月）
    schedules = Schedule.query.filter(
        Schedule.user_id == user.id,
        extract('year', Schedule.start_time) == today.year,
        extract('month', Schedule.start_time) == today.month
    ).all()

    tasks_json = [{
        "id": t.id,
        "title": t.title,
        "planDate": t.plan_date.strftime("%Y-%m-%d") if t.plan_date else "",
        "dueDate": t.due_date.strftime("%Y-%m-%d") if t.due_date else "",
        "priority": t.priority,
        "notes": t.notes,
        "progress": t.progress,
        "status": t.status,
        "tags": t.tag.split(",") if t.tag else []
    } for t in tasks]

    schedules_json = [{
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "startTime": s.start_time.strftime("%Y-%m-%d %H:%M") if s.start_time else "",
        "endTime": s.end_time.strftime("%Y-%m-%d %H:%M") if s.end_time else "",
        "location": s.location,
        "link": s.link
    } for s in schedules]

    input_json = {
        "tasks": tasks_json,
        "schedules": schedules_json
    }
    input_json_str = json.dumps(input_json, ensure_ascii=False, indent=2)

    prompt = MONTHLY_REPORT_PROMPT_TEMPLATE + input_json_str
    try:
        llm_response = generate_content(prompt, "")
        # 尝试从 LLM 返回抽取总结内容
        content = ""
        report_objs = extract_json_from_string(llm_response)
        if isinstance(report_objs, list) and report_objs:
            content = report_objs[0].get("content", "")
        elif isinstance(report_objs, dict):
            content = report_objs.get("content", "")
        else:
            content = str(llm_response)
    except Exception as e:
        return jsonify({"code": 500, "message": "LLM生成失败", "err": str(e)}), 500

    # 写入 monthly_report
    report = MonthlyReport(
        user_id=user.id,
        content=content,
        start_date=month_start,
        end_date=month_end
    )
    db.session.add(report)
    db.session.commit()
    

    return jsonify({
        "code": 200,
        "content": content,
        "start_date": month_start.isoformat(),
        "end_date": month_end.isoformat()
    })

@bp.route("/monthly/history", methods=["GET"])
@login_required()
def get_monthly_reports(user):
    reports = (
        MonthlyReport.query
        .filter_by(user_id=user.id)
        .order_by(MonthlyReport.start_date.desc())
        .all()
    )
    return jsonify([
        {
            "id": r.id,
            "month": f"{r.start_date.strftime('%Y-%m')}",
            "content": r.content
        } for r in reports
    ])
    
@bp.route("/createTask", methods=["POST"])
def create_task():
    try:
        # Get input paragraph
        input_data = request.json
        paragraph = input_data.get("paragraph", "")

        if not paragraph:
            return jsonify({"error": "No paragraph provided"}), 400

        # Call the GenAI service
        response_text = generate_content(TASK_PROMPT_TEMPLATE, paragraph)

        # Parse and return the JSON response
        parsed_response = extract_json_from_string(response_text)
        if parsed_response:
            return jsonify(parsed_response)
        else:
            return jsonify({"error": "Invalid JSON format in AI response", "details": response_text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@bp.route('/weeklyReportGenerate', methods=['POST'])
@login_required()
def generate_weekly_report(current_user):
    """
    生成并保存本周周报
    """
    # 支持传入week参数，否则为本周
    week_date = request.json.get("date")
    if week_date:
        ref_date = datetime.strptime(week_date, "%Y-%m-%d").date()
    else:
        ref_date = datetime.now().date()

    week_start, week_end = get_week_range(ref_date)
    week_str = f"{week_start.year}年第{week_start.isocalendar()[1]}周"
    print(f"本周开始时间: {week_start}, 结束时间: {week_end}")
    # 查询事项（以plan_date为准，已完成和未完成都要）
    tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.plan_date >= week_start,
        Task.plan_date <= week_end
    ).all()

    # 查询日程（以end_time为准）
    schedules = Schedule.query.filter(
        Schedule.user_id == current_user.id,
        Schedule.end_time >= datetime.combine(week_start, datetime.min.time()),
        Schedule.end_time <= datetime.combine(week_end, datetime.max.time())
    ).all()

    # 组装json内容
    tasks_json = [
        {
            "id": t.id,
            "title": t.title,
            "planDate": t.plan_date.strftime("%Y-%m-%d"),
            "dueDate": t.due_date.strftime("%Y-%m-%d"),
            "priority": t.priority,
            "notes": t.notes,
            "status": t.status,
            "progress": t.progress,
            "tags": t.tag.split(",") if t.tag else [],
        }
        for t in tasks
    ]
    schedules_json = [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "startTime": s.start_time.strftime("%Y-%m-%d %H:%M"),
            "endTime": s.end_time.strftime("%Y-%m-%d %H:%M"),
            "location": s.location,
            "link": s.link,
        }
        for s in schedules
    ]
    input_json = {
        "tasks": tasks_json,
        "schedules": schedules_json,
    }

    # 调用大模型生成
    input_json_str = json.dumps(input_json, ensure_ascii=False, indent=2)
    prompt = WEEKLY_PROMPT_TEMPLATE + input_json_str

    llm_response = generate_content(prompt, "")

    # 提取内容
    try:
        report_objs = extract_json_from_string(llm_response)
        content = ""
        if isinstance(report_objs, list) and report_objs:
            content = report_objs[0].get("content", "")
        elif isinstance(report_objs, dict):
            content = report_objs.get("content", "")
        else:
            content = llm_response  # fallback
    except Exception:
        content = llm_response

    # 保存到数据库
    report = WeeklyReport(
        user_id=current_user.id,
        week=week_str,
        content=content
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "周报生成成功",
        "data": {
            "week": week_str,
            "content": content,
            "id": report.id
        }
    })

@bp.route('/weeklyReportHistory', methods=['GET'])
@login_required()
def get_weekly_history(current_user):
    # 查询所有历史周报，按时间降序
    reports = WeeklyReport.query.filter_by(user_id=current_user.id).order_by(WeeklyReport.created_at.desc()).all()
    return jsonify({
        "code": 200,
        "data": [
            {
                "id": r.id,
                "week": r.week,
                "content": r.content
            }
            for r in reports
        ]
    })

@bp.route("/generateSubTasks", methods=["POST"])
def generate_subtasks():
    """
    智能生成子任务（LLM）
    入参：{ "task": { ... } }
    出参：[{"title": ...}, ...]
    """
    try:
        task_json = request.json.get("task")
        if not task_json or not isinstance(task_json, dict):
            return jsonify({"error": "No valid task provided"}), 400

        # 用SUBTASK_PROMPT_TEMPLATE
        import json as _json
        prompt = SUBTASK_PROMPT_TEMPLATE + _json.dumps(task_json, ensure_ascii=False, indent=2)
        response_text = generate_content(prompt, "")
        subtasks = extract_json_from_string(response_text)
        # 确保是列表且格式正确
        if isinstance(subtasks, list) and all("title" in sub for sub in subtasks):
            return jsonify({"code": 200, "data": subtasks})
        else:
            return jsonify({"error": "Invalid LLM JSON", "llm": response_text}), 500
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

