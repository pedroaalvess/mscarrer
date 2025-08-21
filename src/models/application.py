from src.models.user import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Job reference
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    
    # Personal information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    citizenship = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    spi = db.Column(db.String(50), nullable=True)  # Optional field
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Document files
    document_front_filename = db.Column(db.String(200), nullable=False)
    document_back_filename = db.Column(db.String(200), nullable=False)
    address_proof_filename = db.Column(db.String(200), nullable=False)
    
    # Application status
    status = db.Column(db.String(50), default='pending')  # pending, reviewing, accepted, rejected
    notes = db.Column(db.Text, nullable=True)  # Admin notes
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name} for Job {self.job_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'citizenship': self.citizenship,
            'email': self.email,
            'spi': self.spi,
            'phone': self.phone,
            'address': self.address,
            'document_front_filename': self.document_front_filename,
            'document_back_filename': self.document_back_filename,
            'address_proof_filename': self.address_proof_filename,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

