from app import db

class SubTask(db.Model):
    __tablename__ = 'subtask'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    parent_task_id = db.Column(db.BigInteger, db.ForeignKey('task.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.SmallInteger, default=0)