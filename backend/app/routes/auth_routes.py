from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

bp = Blueprint("auth", __name__, url_prefix="/auth")

SECRET_KEY = 'CHRONOS'
TOKEN_EXPIRE_HOURS = 24

@bp.route('/login', methods=['POST'])
def login():
    # 获取正确配置的db实例
    db = current_app.extensions["sqlalchemy"]

    # 延迟导入模型
    from ..models import User

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"code":400, "message":"需要用户名和密码"}),200

    user = db.session.query(User).filter_by(username=data['username']).first()

    # 验证用户存在性
    if not user:
        return jsonify({
            "code": 401,
            "message": "用户名或密码错误"
        }), 200

    # 验证账户状态
    if user.status != 1:
        return jsonify({
            "code": 403,
            "message": "账户已被禁用"
        }), 200

    # 验证密码
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({
            "code": 401,
            "message": "用户名或密码错误"
        })

    try:
        # 生成JWT令牌
        token = jwt.encode({
            'sub': user.id,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS),
            'is_admin': bool(user.is_admin)
        }, SECRET_KEY, algorithm='HS256')

        # 更新用户token和过期时间
        user.token = token
        user.token_expires_at = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
        db.session.commit()

        return jsonify({
            "code": 200,
            "data": {
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "status": user.status,
                    "is_admin": user.is_admin,
                    "token_expires_at": user.token_expires_at.isoformat()
                }
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "令牌存储失败"})


@bp.route('/register',methods=['POST'])
def register():
    from ..models import User

    # 获取数据库实例
    db = current_app.extensions["sqlalchemy"]

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "code": 400,
            "message": "需要用户名和密码"
        }), 200

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
            "code": 201,
            "message": "注册成功",
            "data": {
                "username": new_user.username
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"注册失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "服务器内部错误"
        }), 200

def login_required(admin_required=False):
    """
    登录验证装饰器
    :param admin_required: 是否需要管理员权限
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 从请求头获取Token
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    "code": 401,
                    "message": "无效的授权凭证"
                })

            token = auth_header.split(" ")[1]

            try:
                from ..models import User

                # 查询数据库验证Token
                user = User.query.filter_by(token=token).first()

                # 验证用户是否存在
                if not user:
                    return jsonify({
                        "code": 401,
                        "message": "用户未登录"
                    })

                # 验证账户状态
                if user.status != 1:
                    return jsonify({
                        "code": 403,
                        "message": "账户已被禁用"
                    })

                # 验证Token有效期
                if user.token_expires_at < datetime.utcnow():
                    return jsonify({
                        "code": 401,
                        "message": "登录已过期"
                    })

                # 验证管理员权限
                if admin_required and not user.is_admin:
                    return jsonify({
                        "code": 403,
                        "message": "需要管理员权限"
                    })

                # 将用户对象传递给路由函数
                return f(user, *args, **kwargs)

            except Exception as e:
                return jsonify({
                    "code": 500,
                    "message": "服务器内部错误"
                })

        return wrapper
    return decorator

