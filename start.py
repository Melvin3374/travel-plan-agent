"""
Script de démarrage pour l'assistant voyage IA
Lance tous les composants nécessaires
"""

import os
import sys
import time
import subprocess
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_requirements():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import streamlit
        import langchain
        import google.generativeai
        print("✅ Toutes les dépendances principales sont installées")
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")
        print("💡 Installez les dépendances avec : pip install -r requirements.txt")
        return False
    
    return True

def check_env_variables():
    """Vérifie que les variables d'environnement nécessaires sont définies"""
    print("\n🔐 Vérification des variables d'environnement...")
    
    required_vars = ["GEMINI_API_KEY", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables manquantes : {', '.join(missing_vars)}")
        print("💡 Copiez .env.example vers .env et remplissez les valeurs")
        return False
    
    print("✅ Toutes les variables d'environnement sont configurées")
    return True

def start_database():
    """Démarre la base de données PostgreSQL avec Docker"""
    print("\n🐘 Démarrage de PostgreSQL...")
    
    try:
        # Vérifier si Docker est installé
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        
        # Démarrer PostgreSQL
        subprocess.run(["docker-compose", "up", "-d", "postgres"], check=True)
        
        print("⏳ Attente du démarrage de PostgreSQL...")
        time.sleep(5)  # Attendre que PostgreSQL démarre
        
        print("✅ PostgreSQL est démarré")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Docker n'est pas installé ou n'est pas démarré")
        print("💡 Installez Docker Desktop depuis : https://www.docker.com/products/docker-desktop")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de PostgreSQL : {e}")
        return False

def start_streamlit():
    """Lance l'application Streamlit"""
    print("\n🚀 Lancement de l'application Streamlit...")
    print("📱 L'application va s'ouvrir dans votre navigateur...")
    print("💡 Pour arrêter : Ctrl+C dans ce terminal\n")
    
    try:
        # Lancer Streamlit
        streamlit_path = os.path.join(os.path.dirname(__file__), 'app', 'main.py')
        subprocess.run(["streamlit", "run", streamlit_path])
        
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt de l'application...")
    except Exception as e:
        print(f"❌ Erreur lors du lancement de Streamlit : {e}")

def main():
    """Fonction principale"""
    print("🧳 Assistant IA de Planification de Voyage")
    print("=" * 50)
    
    # Vérifications
    if not check_requirements():
        return
    
    if not check_env_variables():
        return
    
    # Démarrage des services
    if start_database():
        initialize_database()
        
        print("\n✨ Tout est prêt !")
        print("=" * 50)
        
        # Afficher les URLs utiles
        print("\n📍 URLs utiles :")
        print("- Application : http://localhost:8501")
        print("- PgAdmin : http://localhost:5050")
        print("  (Email: admin@travel.com, Password: admin)")
        
        # Lancer Streamlit
        start_streamlit()
    
    # Nettoyage
    print("\n🧹 Arrêt des services...")
    subprocess.run(["docker-compose", "down"], capture_output=True)
    print("✅ Services arrêtés proprement")

if __name__ == "__main__":
    main()