from app import db

class WeeklyReport(db.Model):
    __tablename__ = 'weekly_report'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    week = db.Column(db.String(20), nullable=False)  # 如 "2024年第20周"
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())