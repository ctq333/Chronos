from .. import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.SmallInteger, default=1)
    email = db.Column(db.String(128), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    is_admin = db.Column(db.SmallInteger, default=0)

    # Relationships
    schedules = db.relationship('Schedule', backref='user', cascade="all, delete-orphan", lazy=True)
    tasks = db.relationship('Task', backref='user', cascade="all, delete-orphan", lazy=True)
    sent_invitations = db.relationship('ScheduleInvitation', foreign_keys='ScheduleInvitation.sender_id', backref='sender', cascade="all, delete-orphan", lazy=True)
    received_invitations = db.relationship('ScheduleInvitation', foreign_keys='ScheduleInvitation.receiver_id', backref='receiver', cascade="all, delete-orphan", lazy=True)
    reports = db.relationship('Report', backref='user', cascade="all, delete-orphan", lazy=True)