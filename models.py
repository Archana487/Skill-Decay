from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Skill(db.Model):
    """
    Skill model to represent a user's skill and its usage history.
    """
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    date_learned = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    confidence_score = db.Column(db.Integer, nullable=False)
    actual_score = db.Column(db.Integer, nullable=False)
    
    # Gamification and Tracking
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak = db.Column(db.Integer, default=0)
    last_practice_date = db.Column(db.DateTime, nullable=True)
    
    # Relationship to logs
    logs = db.relationship('PracticeLog', backref='skill', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Skill {self.skill_name}>'

class PracticeLog(db.Model):
    """
    Model to track individual practice sessions for a skill.
    """
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    activity_type = db.Column(db.String(100), nullable=False) # e.g., "Project", "Tutorial", "Quiz"
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<PracticeLog {self.activity_type} for skill {self.skill_id}>'
