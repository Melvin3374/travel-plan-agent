# Fichier : auth/firebase_auth.py

import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
import os
import json
import base64

# --- Configuration Firebase ---
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL") # <-- S'assurer que cette ligne est bien présente
}

# ... le reste du code d'initialisation ne change pas ...
try:
    # ...
    # Le code d'initialisation que nous avons écrit précédemment
    # ...
    firebase = pyrebase.initialize_app(firebase_config)
    firebase_auth = firebase.auth()
    print("✅ Firebase initialisé avec succès")

except Exception as e:
    print(f"❌ Erreur d'initialisation Firebase : {e}")
    firebase_auth = None


# --- Fonctions pour Streamlit (REMETTEZ CETTE VERSION) ---
def signup_user(email, password):
    """Inscrit un nouvel utilisateur avec email/password"""
    if not firebase_auth:
        return None, "Erreur: Firebase n'est pas initialisé correctement."
    try:
        # On utilise le SDK Admin pour créer l'utilisateur (c'est la bonne méthode)
        user = auth.create_user(email=email, password=password)
        return user, "Utilisateur créé avec succès ! Vous pouvez maintenant vous connecter."
    except Exception as e:
        # On retourne l'erreur pour l'afficher dans Streamlit
        return None, f"Erreur lors de l'inscription : {e}"

def login_user(email, password):
    """Connecte un utilisateur avec email/password"""
    if not firebase_auth:
        return None
    try:
        # On utilise Pyrebase pour connecter l'utilisateur
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        return None