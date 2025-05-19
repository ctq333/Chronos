# Import blueprints from individual route files
from app.routes.llm_routes import bp as llm_routes
from app.routes.schedule_routes import bp as schedule_routes
from app.routes.auth_routes import bp as auth_routes
from app.routes.task_routes import bp as task_routes
from app.routes.admin_routes import bp as admin_routes
from app.routes.invitation_routes import bp as invitation_routes

# Expose blueprints for registration in the main app
__all__ = ["llm_routes", "admin_routes", "schedule_routes", "auth_routes", "task_routes", "invitation_routes"]