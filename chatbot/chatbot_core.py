"""
Core du chatbot utilisant LangChain et Gemini
Gère la logique de conversation et la mémoire
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from dotenv import load_dotenv

load_dotenv()

class TravelAssistant:
    """Assistant IA pour la planification de voyage"""
    
    def __init__(self):
        """Initialise l'assistant avec Gemini et LangChain"""
        
        # Configuration Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Mémoire de conversation
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=2000,
            return_messages=True
        )
        
        # Prompt template principal
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un assistant expert en planification de voyage. 
            Tu aides les utilisateurs à créer des itinéraires personnalisés en tenant compte de:
            - Leur style de voyage (backpacker, confort, luxe)
            - Leur budget
            - Leurs intérêts
            - La durée du voyage
            
            Tu fournis des informations détaillées sur:
            - Les étapes du voyage avec timing
            - Les hébergements adaptés au budget
            - Les moyens de transport
            - Les activités et visites
            - Les informations pratiques (visa, vaccins, monnaie)
            - Les tips locaux et bonnes adresses
            - Les précautions à prendre
            
            Sois précis, pratique et enthousiaste !"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
            ("human", "Contexte additionnel: {context}")
        ])
        
        # Chain de conversation
        self.conversation_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=True
        )
        
        # Connexion à la base de données (si disponible)
        self.db = self._init_database()
        
    def _init_database(self) -> Optional[SQLDatabase]:
        """Initialise la connexion à la base de données PostgreSQL"""
        try:
            db_uri = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
            return SQLDatabase.from_uri(db_uri)
        except Exception as e:
            print(f"Attention: Base de données non connectée - {e}")
            return None
    
    def get_response(self, user_input: str, context: str = "", session_id: str = "default") -> str:
        """
        Génère une réponse à la demande de l'utilisateur
        
        Args:
            user_input: Question ou demande de l'utilisateur
            context: Contexte additionnel (préférences, etc.)
            session_id: ID de session pour la mémoire
            
        Returns:
            Réponse de l'assistant
        """
        try:
            # Si on a une base de données, enrichir le contexte
            if self.db:
                db_context = self._search_database(user_input)
                context = f"{context}\n\nInformations de la base de données:\n{db_context}"
            
            # Générer la réponse
            response = self.conversation_chain.run(
                input=user_input,
                context=context
            )
            
            # Sauvegarder la conversation (pour plus tard)
            self._save_conversation(session_id, user_input, response)
            
            return response
            
        except Exception as e:
            return f"Désolé, j'ai rencontré une erreur : {str(e)}. Pouvez-vous reformuler votre demande ?"
    
    def _search_database(self, query: str) -> str:
        """
        Recherche des informations pertinentes dans la base de données
        
        Args:
            query: Requête utilisateur
            
        Returns:
            Informations trouvées formatées
        """
        if not self.db:
            return ""
        
        try:
            # Créer un agent SQL simple
            sql_agent = create_sql_agent(
                llm=self.llm,
                db=self.db,
                verbose=True,
                agent_type="zero-shot-react-description",
            )
            
            # Rechercher les informations pertinentes
            db_query = f"Trouve des informations sur les destinations, hotels ou activités en rapport avec: {query}"
            result = sql_agent.run(db_query)
            
            return result
            
        except Exception as e:
            print(f"Erreur recherche BDD: {e}")
            return ""
    
    def _save_conversation(self, session_id: str, user_input: str, assistant_response: str):
        """
        Sauvegarde la conversation (implémentation basique pour le moment)
        
        Args:
            session_id: ID de la session
            user_input: Message utilisateur
            assistant_response: Réponse de l'assistant
        """
        # Pour le moment, on sauvegarde dans un fichier JSON
        # Plus tard, ce sera dans PostgreSQL
        conversations_file = "conversations.json"
        
        try:
            # Charger les conversations existantes
            if os.path.exists(conversations_file):
                with open(conversations_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
            else:
                conversations = {}
            
            # Ajouter la nouvelle conversation
            if session_id not in conversations:
                conversations[session_id] = []
            
            conversations[session_id].append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "assistant": assistant_response
            })
            
            # Sauvegarder
            with open(conversations_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erreur sauvegarde conversation: {e}")
    
    def get_travel_suggestions(self, destination: str, preferences: Dict) -> List[Dict]:
        """
        Génère des suggestions de voyage basées sur la destination et les préférences
        
        Args:
            destination: Destination souhaitée
            preferences: Préférences utilisateur
            
        Returns:
            Liste de suggestions structurées
        """
        prompt = f"""
        Génère 3 suggestions d'itinéraires pour {destination} avec ces préférences:
        - Style: {preferences.get('travel_style')}
        - Budget: {preferences.get('budget_per_day')}€/jour
        - Intérêts: {preferences.get('interests')}
        
        Pour chaque suggestion, fournis:
        1. Un titre accrocheur
        2. Les points forts de l'itinéraire
        3. Le budget estimé total
        4. La meilleure période pour partir
        
        Formate la réponse en JSON.
        """
        
        try:
            response = self.llm.predict(prompt)
            # Parser et retourner les suggestions
            # (À implémenter avec un parser JSON robuste)
            return []
        except Exception as e:
            print(f"Erreur génération suggestions: {e}")
            return []