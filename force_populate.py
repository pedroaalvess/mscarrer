#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import db
from src.models.job import Job

def force_populate_jobs():
    """Force populate all 6 jobs"""
    
    jobs_data = [
        {
            'title': 'Ingénieur Logiciel Senior - Azure',
            'description': 'Rejoignez notre équipe Azure pour développer des solutions cloud innovantes qui transforment la façon dont les entreprises travaillent. Vous travaillerez sur des projets à grande échelle avec des technologies de pointe.',
            'location': 'Paris, France',
            'department': 'Engineering',
            'employment_type': 'Temps plein',
            'experience_level': 'Senior',
            'requirements': '• Master en informatique ou équivalent\n• 5+ années d\'expérience en développement logiciel\n• Expertise en C#, .NET, Azure\n• Expérience avec les architectures cloud\n• Maîtrise de l\'anglais technique',
            'benefits': '• Salaire compétitif avec bonus\n• Assurance santé premium\n• Télétravail flexible\n• Formation continue\n• Stock options Microsoft\n• 25 jours de congés payés',
            'salary_range': '70 000€ - 95 000€',
            'image_url': '/static/images/azure-engineer.jpg'
        },
        {
            'title': 'Chef de Produit - Microsoft 365',
            'description': 'Dirigez la stratégie produit pour Microsoft 365 et façonnez l\'avenir de la productivité en entreprise. Collaborez avec des équipes internationales pour livrer des fonctionnalités qui impactent des millions d\'utilisateurs.',
            'location': 'Lyon, France',
            'department': 'Product Management',
            'employment_type': 'Temps plein',
            'experience_level': 'Senior',
            'requirements': '• MBA ou Master en gestion de produit\n• 7+ années d\'expérience en product management\n• Expérience avec les produits SaaS\n• Compétences analytiques avancées\n• Leadership et communication excellents',
            'benefits': '• Package de rémunération attractif\n• Assurance santé et dentaire\n• Horaires flexibles\n• Budget formation 5000€/an\n• Participation aux bénéfices\n• Congés sabbatiques',
            'salary_range': '85 000€ - 120 000€',
            'image_url': '/static/images/product-manager.jpg'
        },
        {
            'title': 'Spécialiste Cybersécurité - Defender',
            'description': 'Protégez les données et systèmes de nos clients en développant des solutions de sécurité avancées. Travaillez avec Microsoft Defender pour créer un monde numérique plus sûr.',
            'location': 'Toulouse, France',
            'department': 'Security',
            'employment_type': 'Temps plein',
            'experience_level': 'Intermédiaire',
            'requirements': '• Diplôme en cybersécurité ou informatique\n• 3+ années d\'expérience en sécurité IT\n• Certifications CISSP, CEH ou équivalent\n• Connaissance des menaces cyber actuelles\n• Expérience avec SIEM et SOC',
            'benefits': '• Salaire compétitif\n• Assurance santé complète\n• Télétravail 3 jours/semaine\n• Certifications payées par l\'entreprise\n• Bonus de performance\n• Restaurant d\'entreprise',
            'salary_range': '55 000€ - 75 000€',
            'image_url': '/static/images/cybersecurity.jpg'
        },
        {
            'title': 'Développeur Frontend - Teams',
            'description': 'Créez des expériences utilisateur exceptionnelles pour Microsoft Teams. Travaillez avec React, TypeScript et les dernières technologies web pour connecter le monde du travail.',
            'location': 'Nantes, France',
            'department': 'Engineering',
            'employment_type': 'Temps plein',
            'experience_level': 'Intermédiaire',
            'requirements': '• Licence en informatique ou équivalent\n• 3+ années d\'expérience en développement frontend\n• Expertise React, TypeScript, JavaScript\n• Connaissance des API REST\n• Passion pour l\'UX/UI',
            'benefits': '• Salaire attractif\n• Mutuelle santé premium\n• Flex office et télétravail\n• Équipement high-tech fourni\n• Formations techniques\n• Événements team building',
            'salary_range': '45 000€ - 65 000€',
            'image_url': '/static/images/frontend-dev.jpg'
        },
        {
            'title': 'Data Scientist - Intelligence Artificielle',
            'description': 'Exploitez le pouvoir des données pour créer des solutions d\'IA révolutionnaires. Rejoignez nos équipes de recherche pour développer les technologies de demain.',
            'location': 'Grenoble, France',
            'department': 'AI Research',
            'employment_type': 'Temps plein',
            'experience_level': 'Senior',
            'requirements': '• PhD en Data Science, ML ou domaine connexe\n• 5+ années d\'expérience en IA/ML\n• Expertise Python, TensorFlow, PyTorch\n• Publications scientifiques appréciées\n• Anglais courant requis',
            'benefits': '• Package salarial exceptionnel\n• Assurance santé internationale\n• Budget recherche personnel\n• Conférences internationales\n• Sabbatique recherche\n• Stock options importantes',
            'salary_range': '80 000€ - 110 000€',
            'image_url': '/static/images/data-scientist.jpg'
        },
        {
            'title': 'Responsable Marketing Digital - Xbox',
            'description': 'Développez les stratégies marketing pour Xbox en France. Créez des campagnes innovantes qui connectent les gamers avec leurs jeux préférés et construisent la communauté Xbox.',
            'location': 'Paris, France',
            'department': 'Marketing',
            'employment_type': 'Temps plein',
            'experience_level': 'Senior',
            'requirements': '• Master en marketing digital\n• 6+ années d\'expérience marketing gaming\n• Expertise réseaux sociaux et influenceurs\n• Connaissance de l\'industrie du jeu vidéo\n• Créativité et esprit analytique',
            'benefits': '• Rémunération compétitive\n• Assurance santé premium\n• Accès gratuit Xbox Game Pass\n• Événements gaming exclusifs\n• Horaires flexibles\n• Prime de performance',
            'salary_range': '60 000€ - 85 000€',
            'image_url': '/static/images/xbox-marketing.jpg'
        }
    ]
    
    with app.app_context():
        # Clear ALL jobs
        Job.query.delete()
        db.session.commit()
        print("🗑️ Todas as vagas removidas")
        
        # Add ALL jobs
        for job_data in jobs_data:
            job = Job(**job_data)
            db.session.add(job)
        
        db.session.commit()
        
        # Verify
        count = Job.query.count()
        print(f"✅ {count} vagas adicionadas com sucesso!")
        
        jobs = Job.query.all()
        for job in jobs:
            print(f"  - {job.title} ({job.location})")

if __name__ == '__main__':
    force_populate_jobs()

