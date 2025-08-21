from flask import Blueprint, render_template_string, request, jsonify, session, redirect, url_for
from src.models.user import db
from src.models.job import Job
from src.models.application import Application
import os
from datetime import datetime

admin_access_bp = Blueprint('admin_access', __name__)

# Admin credentials
ADMIN_USERNAME = "microsoft_hr"
ADMIN_PASSWORD = "microsoft_hr_2025"

@admin_access_bp.route('/microsoft-rh-admin-portal')
def admin_portal():
    """Admin portal access page"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portail Administrateur RH - Microsoft France</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0078D4 0%, #106EBE 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo img {
            width: 120px;
            height: auto;
        }
        h1 {
            text-align: center;
            color: #323130;
            margin-bottom: 10px;
            font-size: 24px;
        }
        .subtitle {
            text-align: center;
            color: #605E5C;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #323130;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e1dfdd;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        input:focus {
            outline: none;
            border-color: #0078D4;
            box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.1);
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: #0078D4;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background: #106EBE;
        }
        .error {
            color: #D13438;
            font-size: 14px;
            margin-top: 10px;
            text-align: center;
        }
        .security-note {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 12px;
            color: #605E5C;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <svg width="120" height="30" viewBox="0 0 120 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="14" height="14" fill="#F25022"/>
                <rect x="16" y="0" width="14" height="14" fill="#7FBA00"/>
                <rect x="0" y="16" width="14" height="14" fill="#00A4EF"/>
                <rect x="16" y="16" width="14" height="14" fill="#FFB900"/>
                <text x="40" y="20" font-family="Segoe UI" font-size="16" font-weight="600" fill="#323130">Microsoft</text>
            </svg>
        </div>
        
        <h1>Portail Administrateur</h1>
        <p class="subtitle">Accès réservé au personnel RH Microsoft France</p>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Nom d'utilisateur</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">Se connecter</button>
            
            <div id="error" class="error" style="display: none;"></div>
        </form>
        
        <div class="security-note">
            🔒 Connexion sécurisée - Accès autorisé uniquement
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error');
            
            try {
                const response = await fetch('/microsoft-rh-admin-portal/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = '/microsoft-rh-admin-portal/dashboard';
                } else {
                    errorDiv.textContent = data.error;
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Erreur de connexion';
                errorDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
    ''')

@admin_access_bp.route('/microsoft-rh-admin-portal/login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return jsonify({
                'success': True,
                'message': 'Connexion réussie'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Nom d\'utilisateur ou mot de passe incorrect'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur de connexion'
        }), 500

@admin_access_bp.route('/microsoft-rh-admin-portal/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect('/microsoft-rh-admin-portal')
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard RH - Microsoft France</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }
        .header {
            background: #0078D4;
            color: white;
            padding: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logo svg {
            width: 32px;
            height: 32px;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-4px);
        }
        .stat-number {
            font-size: 48px;
            font-weight: bold;
            color: #0078D4;
            margin-bottom: 10px;
        }
        .stat-label {
            color: #605E5C;
            font-size: 16px;
            font-weight: 600;
        }
        .applications-section {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: #323130;
        }
        .refresh-btn {
            background: #0078D4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        .application-item {
            border-bottom: 1px solid #e1dfdd;
            padding: 20px 0;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 20px;
            align-items: center;
        }
        .application-item:last-child {
            border-bottom: none;
        }
        .application-info h4 {
            margin: 0 0 8px 0;
            font-size: 18px;
            color: #323130;
        }
        .application-info p {
            margin: 0;
            color: #605E5C;
            font-size: 14px;
        }
        .application-actions {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .status {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .status.pending { background: #fff4e6; color: #d68910; }
        .status.reviewing { background: #e6f3ff; color: #0078D4; }
        .status.accepted { background: #e6f7e6; color: #107C10; }
        .status.rejected { background: #ffe6e6; color: #D13438; }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: opacity 0.3s ease;
        }
        .btn:hover { opacity: 0.9; }
        .btn-primary { background: #0078D4; color: white; }
        .btn-secondary { background: #f3f2f1; color: #323130; }
        .loading {
            text-align: center;
            padding: 40px;
            color: #605E5C;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #605E5C;
        }
        .empty-state svg {
            width: 64px;
            height: 64px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="15" height="15" fill="white"/>
                    <rect x="17" y="0" width="15" height="15" fill="white"/>
                    <rect x="0" y="17" width="15" height="15" fill="white"/>
                    <rect x="17" y="17" width="15" height="15" fill="white"/>
                </svg>
                <div>
                    <h1>Dashboard RH</h1>
                    <p>Microsoft France</p>
                </div>
            </div>
            <div class="user-info">
                <span>Connecté en tant que: <strong>{{ session.admin_username }}</strong></span>
                <button class="logout-btn" onclick="logout()">Déconnexion</button>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="stats" id="statsContainer">
            <div class="stat-card">
                <div class="stat-number" id="totalJobs">-</div>
                <div class="stat-label">Offres d'emploi</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalApplications">-</div>
                <div class="stat-label">Candidatures totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="pendingApplications">-</div>
                <div class="stat-label">En attente</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="activeJobs">-</div>
                <div class="stat-label">Postes actifs</div>
            </div>
        </div>

        <div class="applications-section">
            <div class="section-header">
                <h2 class="section-title">Candidatures récentes</h2>
                <button class="refresh-btn" onclick="loadData()">Actualiser</button>
            </div>
            <div id="applicationsContainer" class="loading">
                Chargement des candidatures...
            </div>
        </div>
    </div>

    <script>
        // Load data on page load
        loadData();

        async function loadData() {
            try {
                // Load stats
                const statsResponse = await fetch('/microsoft-rh-admin-portal/api/stats');
                const statsData = await statsResponse.json();
                
                if (statsData.success) {
                    document.getElementById('totalJobs').textContent = statsData.stats.total_jobs;
                    document.getElementById('totalApplications').textContent = statsData.stats.total_applications;
                    document.getElementById('pendingApplications').textContent = statsData.stats.pending_applications;
                    document.getElementById('activeJobs').textContent = statsData.stats.active_jobs;
                }
                
                // Load applications
                const appsResponse = await fetch('/microsoft-rh-admin-portal/api/applications');
                const appsData = await appsResponse.json();
                
                if (appsData.success) {
                    displayApplications(appsData.applications);
                }
            } catch (error) {
                console.error('Error loading data:', error);
                document.getElementById('applicationsContainer').innerHTML = '<div class="empty-state">Erreur de chargement des données</div>';
            }
        }
        
        function displayApplications(applications) {
            const container = document.getElementById('applicationsContainer');
            
            if (applications.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19Z"/>
                            <path d="M7 7H17V9H7V7ZM7 11H17V13H7V11ZM7 15H13V17H7V15Z"/>
                        </svg>
                        <h3>Aucune candidature</h3>
                        <p>Les nouvelles candidatures apparaîtront ici</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = applications.map(app => `
                <div class="application-item">
                    <div class="application-info">
                        <h4>${app.first_name} ${app.last_name}</h4>
                        <p>${app.job_title} • ${app.email} • ${new Date(app.created_at).toLocaleDateString('fr-FR')}</p>
                    </div>
                    <div class="application-actions">
                        <span class="status ${app.status}">${getStatusText(app.status)}</span>
                        <button class="btn btn-primary" onclick="viewApplication(${app.id})">Détails</button>
                        <button class="btn btn-secondary" onclick="downloadDocuments(${app.id})">Documents</button>
                    </div>
                </div>
            `).join('');
        }
        
        function getStatusText(status) {
            const statusMap = {
                'pending': 'En attente',
                'reviewing': 'En cours',
                'accepted': 'Accepté',
                'rejected': 'Rejeté'
            };
            return statusMap[status] || status;
        }
        
        async function viewApplication(id) {
            try {
                const response = await fetch(`/microsoft-rh-admin-portal/api/applications/${id}`);
                const data = await response.json();
                
                if (data.success) {
                    const app = data.application;
                    alert(`Détails de la candidature:
                    
Nom: ${app.first_name} ${app.last_name}
Email: ${app.email}
Téléphone: ${app.phone}
Date de naissance: ${app.birth_date}
Nationalité: ${app.citizenship}
Adresse: ${app.address}
SPI: ${app.spi || 'Non renseigné'}
Poste: ${app.job_title}
Statut: ${getStatusText(app.status)}
Date de candidature: ${new Date(app.created_at).toLocaleDateString('fr-FR')}
                    `);
                }
            } catch (error) {
                alert('Erreur lors du chargement des détails');
            }
        }
        
        async function downloadDocuments(id) {
            const types = ['document_front', 'document_back', 'address_proof'];
            const names = ['Document recto', 'Document verso', 'Justificatif de domicile'];
            
            for (let i = 0; i < types.length; i++) {
                try {
                    const response = await fetch(`/microsoft-rh-admin-portal/api/applications/${id}/download/${types[i]}`);
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `${names[i]}_${id}`;
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }
                } catch (error) {
                    console.error(`Error downloading ${types[i]}:`, error);
                }
            }
        }
        
        async function logout() {
            try {
                await fetch('/microsoft-rh-admin-portal/logout', { method: 'POST' });
                window.location.href = '/microsoft-rh-admin-portal';
            } catch (error) {
                window.location.href = '/microsoft-rh-admin-portal';
            }
        }
    </script>
</body>
</html>
    ''')

@admin_access_bp.route('/microsoft-rh-admin-portal/logout', methods=['POST'])
def admin_logout():
    """Handle admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({'success': True})

# API routes for admin dashboard
@admin_access_bp.route('/microsoft-rh-admin-portal/api/stats')
def api_stats():
    """Get admin dashboard statistics"""
    if not session.get('admin_logged_in'):
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

@admin_access_bp.route('/microsoft-rh-admin-portal/api/applications')
def api_applications():
    """Get all applications"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        applications = Application.query.order_by(Application.created_at.desc()).limit(20).all()
        
        applications_data = []
        for app in applications:
            app_data = app.to_dict()
            job = Job.query.get(app.job_id)
            app_data['job_title'] = job.title if job else 'Poste supprimé'
            applications_data.append(app_data)
        
        return jsonify({
            'success': True,
            'applications': applications_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_access_bp.route('/microsoft-rh-admin-portal/api/applications/<int:application_id>')
def api_application_details(application_id):
    """Get detailed application information"""
    if not session.get('admin_logged_in'):
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

@admin_access_bp.route('/microsoft-rh-admin-portal/api/applications/<int:application_id>/download/<file_type>')
def api_download_file(application_id, file_type):
    """Download application files"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        from flask import send_from_directory, current_app
        
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

