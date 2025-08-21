from flask import Blueprint, request, jsonify, send_from_directory, current_app
from src.models.user import db
from src.models.job import Job
from src.models.application import Application
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Simple authentication check (in production, use proper authentication)
ADMIN_SECRET = "microsoft_hr_2025"

def check_admin_auth():
    """Simple admin authentication check"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {ADMIN_SECRET}":
        return False
    return True

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        password = data.get('password')
        
        if password == ADMIN_SECRET:
            return jsonify({
                'success': True,
                'token': ADMIN_SECRET,
                'message': 'Connexion réussie'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Mot de passe incorrect'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/applications', methods=['GET'])
def get_applications():
    """Get all applications with pagination"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status_filter = request.args.get('status')
        job_id_filter = request.args.get('job_id', type=int)
        
        query = Application.query
        
        # Apply filters
        if status_filter:
            query = query.filter_by(status=status_filter)
        if job_id_filter:
            query = query.filter_by(job_id=job_id_filter)
        
        # Order by creation date (newest first)
        query = query.order_by(Application.created_at.desc())
        
        # Paginate
        applications = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Get job titles for each application
        applications_data = []
        for app in applications.items:
            app_data = app.to_dict()
            job = Job.query.get(app.job_id)
            app_data['job_title'] = job.title if job else 'Poste supprimé'
            applications_data.append(app_data)
        
        return jsonify({
            'success': True,
            'applications': applications_data,
            'pagination': {
                'page': applications.page,
                'pages': applications.pages,
                'per_page': applications.per_page,
                'total': applications.total,
                'has_next': applications.has_next,
                'has_prev': applications.has_prev
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/applications/<int:application_id>', methods=['GET'])
def get_application_details(application_id):
    """Get detailed application information"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        application = Application.query.get_or_404(application_id)
        job = Job.query.get(application.job_id)
        
        app_data = application.to_dict()
        app_data['job_title'] = job.title if job else 'Poste supprimé'
        app_data['job_department'] = job.department if job else None
        
        return jsonify({
            'success': True,
            'application': app_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Update application status"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        application = Application.query.get_or_404(application_id)
        data = request.get_json()
        
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if new_status not in ['pending', 'reviewing', 'accepted', 'rejected']:
            return jsonify({
                'success': False,
                'error': 'Statut invalide'
            }), 400
        
        application.status = new_status
        application.notes = notes
        application.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Statut mis à jour avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/applications/<int:application_id>/download/<file_type>')
def download_application_file(application_id, file_type):
    """Download application files"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        application = Application.query.get_or_404(application_id)
        
        filename_map = {
            'document_front': application.document_front_filename,
            'document_back': application.document_back_filename,
            'address_proof': application.address_proof_filename
        }
        
        if file_type not in filename_map:
            return jsonify({'success': False, 'error': 'Type de fichier invalide'}), 400
        
        filename = filename_map[file_type]
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'applications')
        
        return send_from_directory(
            upload_folder, 
            filename, 
            as_attachment=True,
            download_name=f"{application.get_full_name()}_{file_type}.{filename.split('.')[-1]}"
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/jobs', methods=['GET'])
def get_admin_jobs():
    """Get all jobs for admin"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        jobs = Job.query.order_by(Job.created_at.desc()).all()
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/jobs', methods=['POST'])
def create_job():
    """Create new job posting"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'location', 'department', 'employment_type', 'experience_level', 'requirements', 'benefits']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        job = Job(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            department=data['department'],
            employment_type=data['employment_type'],
            experience_level=data['experience_level'],
            requirements=data['requirements'],
            benefits=data['benefits'],
            salary_range=data.get('salary_range', ''),
            image_url=data.get('image_url', '')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Offre d\'emploi créée avec succès',
            'job_id': job.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin dashboard statistics"""
    if not check_admin_auth():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        total_jobs = Job.query.count()
        active_jobs = Job.query.filter_by(is_active=True).count()
        total_applications = Application.query.count()
        pending_applications = Application.query.filter_by(status='pending').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'pending_applications': pending_applications
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

