# Fichier : auth/firebase_auth.py

import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
import os
import json # Import nécessaire

# --- Configuration Firebase (ne change pas) ---
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    # ... (le reste de votre config)
}

# --- NOUVELLE LOGIQUE D'INITIALISATION (pour le déploiement) ---
try:
    # On essaie de lire le secret depuis les variables d'environnement (pour Streamlit Cloud)
    firebase_secret_json_str = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if firebase_secret_json_str:
        # Si on le trouve, on le convertit de texte en dictionnaire Python
        firebase_secret_json = json.loads(firebase_secret_json_str)
        cred = credentials.Certificate(firebase_secret_json)
    else:
        # Sinon (en local), on lit le fichier comme avant
        cred = credentials.Certificate("firebase-service-account.json")

    # On vérifie que Firebase n'est pas déjà initialisé (important pour Streamlit)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    firebase = pyrebase.initialize_app(firebase_config)
    firebase_auth = firebase.auth()
    print("✅ Firebase initialisé avec succès")

except Exception as e:
    print(f"❌ Erreur d'initialisation Firebase : {e}")
    firebase_auth = None

# --- Fonctions pour Streamlit (ne changent pas) ---
def signup_user(email, password):
    # ... (votre fonction signup_user reste la même)
    pass

def login_user(email, password):
    # ... (votre fonction login_user reste la même)
    pass