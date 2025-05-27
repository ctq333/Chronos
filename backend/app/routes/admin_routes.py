from flask import Blueprint, jsonify, request, abort, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from app.routes.auth_routes import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")
bcrypt = Bcrypt()
@bp.route("/users", methods=["GET"])
@login_required(admin_required=True)
def get_users(user):
    db = current_app.extensions["sqlalchemy"]

    from ..models.user import User
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "status": user.status,
                "is_admin": user.is_admin
            })

        return jsonify({"code":200, "users": users_data})

    except SQLAlchemyError as e:
        # 数据库错误处理
        db.session.rollback()
        return jsonify({"code":500, "message": "获取用户失败"})
@bp.route("/users", methods=["POST"])
@login_required(admin_required=True)
def create_user(user):
    db = current_app.extensions["sqlalchemy"]
    from ..models.user import User

    data = request.get_json()
    required_fields = ["username", "password"]

    # 验证必填参数
    for field in required_fields:
        if not data.get(field):
            return jsonify({"code":400,"message": f"缺少必填字段：{field}"})

    username = data['username'].strip()
    password = data['password'].strip()

    # 检查用户名是否存在
    if db.session.query(User).filter_by(username=username).first():
        return jsonify({
            "code": 409,
            "message": "用户名已被注册"
        }), 200

    try:
        from werkzeug.security import generate_password_hash

        # 创建新用户
        new_user = User(
            username=username,
            password_hash=generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=16
            ),
            email=data.get('email'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "新建成功",
            "data": {
                "username": new_user.username
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"新建失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "服务器内部错误"
        }), 200
@bp.route("/users/<int:user_id>/status", methods=["PUT"])
@login_required(admin_required=True)
def update_user(current_user, user_id):
    db = current_app.extensions["sqlalchemy"]
    from ..models.user import User

    target_user = User.query.get_or_404(user_id)


    # 禁止禁用自己
    if target_user.id == current_user.id:
        return jsonify({
            "code": 403,
            "message": "不能修改自己的账户状态"
        })
    
    # 禁止禁用其他管理员账户
    if target_user.is_admin:
        print(target_user.is_admin)
        return jsonify({
            "code": 403,
            "message": "不能修改其他管理员账户状态"
        }), 200

    if target_user.status == 1:
        target_user.status = 0
    else:
        target_user.status = 1

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"code":500, "message": "数据库操作失败"})

    return jsonify({
        "code":200,
        "id": target_user.id
    })
@bp.route("/users/<int:user_id>/password", methods=["PUT"])
@login_required(admin_required=True)
def reset_user_password(user, user_id):
    db = current_app.extensions["sqlalchemy"]
    from ..models.user import User

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data or "new_password" not in data:
        return jsonify({"code":400, "message": "缺少新密码参数"})

    from werkzeug.security import generate_password_hash

    user.password_hash=generate_password_hash(
        data["new_password"],
        method='pbkdf2:sha256',
        salt_length=16
    ),
    user.updated_at = datetime.utcnow()  # 更新最后修改时间

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"code":500,"message": "数据库操作失败"})

    return jsonify({"code":200,"message": "密码重置成功"})

@bp.route("/users/<int:user_id>", methods=["DELETE"])
@login_required(admin_required=True)
def delete_user(user, user_id):
    db = current_app.extensions["sqlalchemy"]
    from ..models.user import User

    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"code":409,"message": "该用户存在关联数据，无法删除"})

    return jsonify({"code":200,"message": "用户删除成功"})

@bp.route("/users/batch", methods=["DELETE"])
@login_required(admin_required=True)
def batch_delete_users(user):
    db = current_app.extensions["sqlalchemy"]
    from ..models.user import User

    data = request.get_json()
    if not data or "user_ids" not in data:
        return jsonify({"code":400,"message": "缺少用户ID列表"})

    users = User.query.filter(User.id.in_(data["user_ids"])).all()
    if not users:
        return jsonify({"code":404,"message": "未找到指定用户"})

    try:
        for user in users:
            db.session.delete(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"code":409,"message": "部分用户存在关联数据，删除失败"})

    return jsonify({"code":200,"message": f"成功删除 {len(users)} 个用户"})