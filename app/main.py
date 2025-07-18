# Fichier : app/main.py (Version finale avec authentification)

import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# On importe les nouvelles fonctions d'authentification et l'agent
from agent.travel_agent import get_response
from auth.firebase_auth import signup_user, login_user


# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="🧳 Assistant Voyage IA",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FONCTION POUR L'ÉCRAN DE CONNEXION ---
def show_login_page():
    st.title("Bienvenue sur votre Assistant de Voyage 🧳")
    st.header("Connexion / Inscription")
    
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Se connecter"):
            user = login_user(email, password)
            if user:
                st.session_state['user_info'] = user # Stocker les infos utilisateur
                st.success("Connexion réussie !")
                st.rerun() # Recharger la page pour afficher l'app principale
            else:
                st.error("Email ou mot de passe incorrect.")

    with col2:
        if st.button("S'inscrire"):
            user, message = signup_user(email, password)
            if user:
                st.success(message)
            else:
                st.error(message)

# --- FONCTION POUR L'APPLICATION PRINCIPALE (VOTRE CODE ACTUEL) ---
def show_main_app():
    # Initialisation de la session pour le chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Titre et description
    st.title("🧳 Assistant IA de Planification de Voyage")
    st.markdown("Bienvenue ! Je suis votre assistant personnel pour planifier vos voyages sur mesure.")

    # Sidebar pour les préférences et la déconnexion
    with st.sidebar:
        st.header("⚙️ Préférences de voyage")
        travel_style = st.selectbox("Votre style de voyage", ["Confort (hôtels, voiture)", "Backpacker (auberges, transports locaux)"])
        budget_range = st.select_slider("Budget par jour (€)", options=[30, 50, 100, 200, 500], value=100)
        duration = st.number_input("Durée du voyage (jours)", min_value=1, value=7)
        interests = st.multiselect("Vos intérêts", ["Culture", "Gastronomie", "Nature", "Sport", "Plage"])

        if st.button("💾 Appliquer mes préférences"):
            preferences_text = (
                f"(Note : planifier un voyage avec les préférences suivantes : "
                f"Style: {travel_style}, Budget: {budget_range}€/jour, Durée: {duration} jours, Intérêts: {', '.join(interests)})"
            )
            st.session_state.messages.append({"role": "user", "content": preferences_text})
            st.success("Préférences prises en compte !")

        st.divider()
        if st.button("Se déconnecter"):
            del st.session_state['user_info']
            st.rerun()

    # Zone de chat principale
    st.divider()
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Où souhaitez-vous voyager ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("L'agent réfléchit..."):
                response = get_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- ROUTEUR PRINCIPAL ---
# C'est ce bloc qui décide quelle page afficher
if 'user_info' in st.session_state and st.session_state.user_info is not None:
    show_main_app()
else:
    show_login_page()