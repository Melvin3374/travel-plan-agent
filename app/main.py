"""
Assistant IA de Planification de Voyage
Interface Streamlit principale
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.chatbot_core import TravelAssistant
from database.postgres_db import DatabaseManager

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="🧳 Assistant Voyage IA",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "travel_assistant" not in st.session_state:
    st.session_state.travel_assistant = TravelAssistant()
    
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {}

# Titre et description
st.title("🧳 Assistant IA de Planification de Voyage")
st.markdown("""
Bienvenue ! Je suis votre assistant personnel pour planifier vos voyages sur mesure.
Dites-moi simplement où vous souhaitez aller et je m'occupe du reste ! 🌍
""")

# Sidebar pour les préférences
with st.sidebar:
    st.header("⚙️ Préférences de voyage")
    
    # Type de voyageur
    travel_style = st.selectbox(
        "Votre style de voyage",
        ["Confort (hôtels, voiture)", "Backpacker (auberges, transports locaux)", 
         "Luxe (5 étoiles)", "Aventurier (camping, trek)"]
    )
    
    # Budget
    budget_range = st.select_slider(
        "Budget par jour (€)",
        options=[30, 50, 100, 200, 500, 1000],
        value=100
    )
    
    # Durée
    duration = st.number_input(
        "Durée du voyage (jours)",
        min_value=1,
        max_value=365,
        value=7
    )
    
    # Intérêts
    interests = st.multiselect(
        "Vos intérêts",
        ["Culture", "Gastronomie", "Nature", "Sport", "Plage", 
         "Shopping", "Vie nocturne", "Histoire", "Photographie"]
    )
    
    # Sauvegarder les préférences
    if st.button("💾 Sauvegarder mes préférences"):
        st.session_state.user_preferences = {
            "travel_style": travel_style,
            "budget_per_day": budget_range,
            "interests": interests
        }
        st.success("Préférences sauvegardées !")

# Zone de chat principale
st.divider()

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Où souhaitez-vous voyager ? Décrivez votre voyage idéal..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Afficher le message de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis à votre voyage idéal..."):
            # Construire le contexte avec les préférences
            context = f"""
            Préférences utilisateur:
            - Style: {st.session_state.user_preferences.get('travel_style', 'Non défini')}
            - Budget: {st.session_state.user_preferences.get('budget_per_day', 'Non défini')}€/jour
            - Intérêts: {', '.join(st.session_state.user_preferences.get('interests', []))}
            - Durée souhaitée: {duration} jours
            
            Demande: {prompt}
            """
            
            # Obtenir la réponse de l'assistant
            response = st.session_state.travel_assistant.get_response(
                user_input=prompt,
                context=context,
                session_id=st.session_state.get('session_id', 'default')
            )
            
            # Afficher la réponse
            st.markdown(response)
            
            # Ajouter à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer avec informations
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🔒 Vos données sont sécurisées")
    
with col2:
    st.caption("🤖 Propulsé par Gemini AI")
    
with col3:
    if st.button("🗑️ Nouvelle conversation"):
        st.session_state.messages = []
        st.rerun()