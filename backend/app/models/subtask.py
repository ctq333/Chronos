<<<<<<< HEAD
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base
=======
from app import db
>>>>>>> bc01a6e07acce1995235be4dc2eaa8d1131ad045

class SubTask(Base):
    __tablename__ = 'subtask'

    id = Column(Integer, primary_key=True, index=True)
    main_task_id = Column(String(64), nullable=False) 
    task_id = Column(String(64), nullable=False)       
    title = Column(String(255), nullable=False)
    description = Column(String(1024))
    have_deadline = Column(Boolean, default=False)
    deadline = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)

    def set_completed(self):
        self.is_completed = True

    def set_not_completed(self):
        self.is_completed = False


    def to_dict(self):
        return {
            "id": self.id,
            "mainTaskId": self.main_task_id,
            "taskId": self.task_id,
            "title": self.title,
            "description": self.description,
            "haveDeadline": self.have_deadline,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "isCompleted": self.is_completed
        }
