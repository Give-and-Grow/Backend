#Backend/app/models/participant_attendance.py
from ..extensions import db
import enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.models.opportunity_day import OpportunityDay

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXCUSED = "excused"
    LATE = "late"

class ParticipantAttendance(db.Model):
    __tablename__ = "participant_attendance"
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("opportunity_participant.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(AttendanceStatus), nullable=False)
    
    participant = db.relationship("OpportunityParticipant", back_populates="attendance_records")
