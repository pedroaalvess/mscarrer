from src.models.user import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False)  # Full-time, Part-time, Contract
    experience_level = db.Column(db.String(50), nullable=False)  # Entry, Mid, Senior
    requirements = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with applications
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'department': self.department,
            'employment_type': self.employment_type,
            'experience_level': self.experience_level,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'salary_range': self.salary_range,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

