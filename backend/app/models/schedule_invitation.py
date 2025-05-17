from app import db

class ScheduleInvitation(db.Model):
    __tablename__ = 'schedule_invitation'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.BigInteger, db.ForeignKey('schedule.id', ondelete="CASCADE"), nullable=False)
    sender_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    status = db.Column(db.SmallInteger, default=0, nullable=False)