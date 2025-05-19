from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}?charset=utf8mb4"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 在初始化 db 之后，再导入模型和蓝图，避免循环导入
    from app.models import User, Schedule, Task, ScheduleInvitation, SubTask, Report

    # Register blueprints (导入蓝图对象并注册)
    from app.routes import llm_routes, admin_routes, auth_routes, task_routes, schedule_routes, invitation_routes
    app.register_blueprint(llm_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(task_routes)
    app.register_blueprint(schedule_routes)
    app.register_blueprint(invitation_routes)

    # CORS configuration
    allowed_origins = os.getenv("ALLOWED_CORS_ORIGINS", "*").split(",")
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    return app