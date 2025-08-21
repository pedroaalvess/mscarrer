#!/usr/bin/env python3
"""
Script para backup e restore do banco de dados Microsoft Jobs
"""
import os
import sys
import sqlite3
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def backup_database():
    """Cria backup do banco de dados em JSON"""
    db_path = os.path.join(os.path.dirname(__file__), 'microsoft_jobs.db')
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'applications': [],
            'jobs': []
        }
        
        # Backup applications
        cursor.execute("SELECT * FROM application")
        applications = cursor.fetchall()
        for app in applications:
            backup_data['applications'].append(dict(app))
        
        # Backup jobs
        cursor.execute("SELECT * FROM job")
        jobs = cursor.fetchall()
        for job in jobs:
            backup_data['jobs'].append(dict(job))
        
        conn.close()
        
        # Save backup
        backup_filename = f"backup_microsoft_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Backup criado: {backup_filename}")
        print(f"📊 {len(backup_data['applications'])} candidaturas salvas")
        print(f"📊 {len(backup_data['jobs'])} vagas salvas")
        return True
        
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return False

def restore_database(backup_file):
    """Restaura banco de dados a partir de backup JSON"""
    if not os.path.exists(backup_file):
        print(f"❌ Arquivo de backup não encontrado: {backup_file}")
        return False
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        db_path = os.path.join(os.path.dirname(__file__), 'microsoft_jobs.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM application")
        cursor.execute("DELETE FROM job")
        
        # Restore jobs
        for job in backup_data.get('jobs', []):
            placeholders = ', '.join(['?' for _ in job.values()])
            columns = ', '.join(job.keys())
            cursor.execute(f"INSERT INTO job ({columns}) VALUES ({placeholders})", list(job.values()))
        
        # Restore applications
        for app in backup_data.get('applications', []):
            placeholders = ', '.join(['?' for _ in app.values()])
            columns = ', '.join(app.keys())
            cursor.execute(f"INSERT INTO application ({columns}) VALUES ({placeholders})", list(app.values()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Banco restaurado de: {backup_file}")
        print(f"📊 {len(backup_data.get('applications', []))} candidaturas restauradas")
        print(f"📊 {len(backup_data.get('jobs', []))} vagas restauradas")
        return True
        
    except Exception as e:
        print(f"❌ Erro na restauração: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python backup_restore.py backup")
        print("  python backup_restore.py restore <arquivo_backup.json>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "backup":
        backup_database()
    elif command == "restore" and len(sys.argv) == 3:
        restore_database(sys.argv[2])
    else:
        print("❌ Comando inválido!")
        print("Uso:")
        print("  python backup_restore.py backup")
        print("  python backup_restore.py restore <arquivo_backup.json>")

