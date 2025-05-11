from .. import db

class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    link = db.Column(db.String(255))

    # Relationships
    invitations = db.relationship('ScheduleInvitation', backref='schedule', cascade="all, delete-orphan", lazy=True)