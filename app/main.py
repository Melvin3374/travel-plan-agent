# Fichier : app/main.py (version finale avec gestion du contexte par la mémoire)

import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.travel_agent import get_response

load_dotenv()

st.set_page_config(
    page_title="🧳 Assistant Voyage IA",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Pas de changement ici ---
st.title("🧳 Assistant IA de Planification de Voyage")
st.markdown("""
Bienvenue ! Je suis votre assistant personnel pour planifier vos voyages sur mesure.
Dites-moi simplement où vous souhaitez aller et je m'occupe du reste ! 🌍
""")

with st.sidebar:
    st.header("⚙️ Préférences de voyage")
    travel_style = st.selectbox("Votre style de voyage", ["Confort (hôtels, voiture)", "Backpacker (auberges, transports locaux)", "Luxe (5 étoiles)", "Aventurier (camping, trek)"])
    budget_range = st.select_slider("Budget par jour (€)", options=[30, 50, 100, 200, 500, 1000], value=100)
    duration = st.number_input("Durée du voyage (jours)", min_value=1, max_value=365, value=7)
    interests = st.multiselect("Vos intérêts", ["Culture", "Gastronomie", "Nature", "Sport", "Plage", "Shopping", "Vie nocturne", "Histoire", "Photographie"])

    # --- CHANGEMENT 1 : On injecte les préférences dans la mémoire de l'agent ---
    if st.button("💾 Appliquer mes préférences"):
        preferences_text = (
            f"(Note pour moi-même : je dois planifier un voyage en tenant compte des préférences suivantes : "
            f"Style de voyage: {travel_style}, "
            f"Budget journalier: {budget_range}€, "
            f"Durée: {duration} jours, "
            f"Intérêts: {', '.join(interests)}. "
            f"Je dois utiliser ces informations pour les prochaines réponses.)"
        )
        # On ajoute un message système à l'historique pour que l'agent en soit conscient
        st.session_state.messages.append({"role": "user", "content": preferences_text})
        st.success("Préférences prises en compte pour la conversation !")

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Où souhaitez-vous voyager ? Décrivez votre voyage idéal..."):
    prompt = prompt.replace("<", "&lt;").replace(">", "&gt;")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("L'agent réfléchit à votre voyage..."):
            
            # --- CHANGEMENT 2 : On appelle l'agent UNIQUEMENT avec la question directe ---
            response = get_response(prompt)
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- Pas de changement ici ---
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