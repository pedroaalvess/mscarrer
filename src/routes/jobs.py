from flask import Blueprint, request, jsonify, current_app
from src.models.user import db
from src.models.job import Job
from src.models.application import Application
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

# Allowed file extensions for document uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """Save uploaded file with unique filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return unique_filename
    return None

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all active jobs"""
    try:
        jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job by ID"""
    try:
        job = Job.query.get_or_404(job_id)
        if not job.is_active:
            return jsonify({
                'success': False,
                'error': 'Job not found or inactive'
            }), 404
            
        return jsonify({
            'success': True,
            'job': job.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@jobs_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
def apply_for_job(job_id):
    """Submit job application"""
    try:
        # Check if job exists and is active
        job = Job.query.get_or_404(job_id)
        if not job.is_active:
            return jsonify({
                'success': False,
                'error': 'Cette offre d\'emploi n\'est plus disponible'
            }), 404

        # Get form data
        data = request.form
        files = request.files

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'birth_date', 'citizenship', 'email', 'phone', 'address']
        missing_fields = []
        for field in required_fields:
            if not data.get(field) or not data.get(field).strip():
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Champs requis manquants: {", ".join(missing_fields)}'
            }), 400

        # Validate required files
        required_files = ['document_front', 'document_back', 'address_proof']
        missing_files = []
        for file_key in required_files:
            if file_key not in files or not files[file_key] or not files[file_key].filename:
                missing_files.append(file_key)
        
        if missing_files:
            return jsonify({
                'success': False,
                'error': f'Fichiers requis manquants: {", ".join(missing_files)}'
            }), 400

        # Create upload directory
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'applications')
        
        # Save uploaded files
        document_front_filename = save_uploaded_file(files['document_front'], upload_folder)
        document_back_filename = save_uploaded_file(files['document_back'], upload_folder)
        address_proof_filename = save_uploaded_file(files['address_proof'], upload_folder)

        if not all([document_front_filename, document_back_filename, address_proof_filename]):
            return jsonify({
                'success': False,
                'error': 'Erreur lors du téléchargement des fichiers'
            }), 400

        # Parse birth date (DD/MM/YYYY format)
        try:
            # Convert DD/MM/YYYY to YYYY-MM-DD for database
            birth_date_str = data['birth_date']
            if '/' in birth_date_str:
                day, month, year = birth_date_str.split('/')
                birth_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
            else:
                birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Format de date de naissance invalide. Utilisez JJ/MM/AAAA'
            }), 400

        # Create application
        application = Application(
            job_id=job_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=birth_date,
            citizenship=data['citizenship'],
            email=data['email'],
            spi=data.get('spi', ''),  # Optional field
            phone=data['phone'],
            address=data['address'],
            document_front_filename=document_front_filename,
            document_back_filename=document_back_filename,
            address_proof_filename=address_proof_filename
        )

        db.session.add(application)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Votre candidature a été soumise avec succès',
            'application_id': application.id
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in job application: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de l\'envoi de la candidature. Veuillez réessayer.'
        }), 500

@jobs_bp.route('/jobs/departments', methods=['GET'])
def get_departments():
    """Get all unique departments"""
    try:
        departments = db.session.query(Job.department).filter_by(is_active=True).distinct().all()
        return jsonify({
            'success': True,
            'departments': [dept[0] for dept in departments]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

