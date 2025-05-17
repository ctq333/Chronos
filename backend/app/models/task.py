from app import db

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    plan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.SmallInteger, default=2)
    notes = db.Column(db.String(255))
    progress = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=0)
    postpone_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    tag = db.Column(db.String(255))

    # Relationships
    subtasks = db.relationship('SubTask', backref='parent_task', cascade="all, delete-orphan", lazy=True)