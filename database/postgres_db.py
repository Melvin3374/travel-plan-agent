"""
Gestionnaire de base de données PostgreSQL
Gère les tables et les opérations CRUD
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager
from langchain_community.utilities import SQLDatabase

load_dotenv()

class DatabaseManager:
    """Gestionnaire pour la base de données PostgreSQL"""
    
    def __init__(self):
        """Initialise la connexion à la base de données"""
        self.connection_params = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
            "database": os.getenv("POSTGRES_DB", "travel_assistant"),
            "user": os.getenv("POSTGRES_USER", "travel_user"),
            "password": os.getenv("POSTGRES_PASSWORD", "")
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager pour gérer les connexions à la base de données"""
        conn = psycopg2.connect(**self.connection_params)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def insert_activity(self, activity_data: Dict) -> int:
        """Insère une nouvelle activité"""
        query = """
        INSERT INTO activities
        (destination_id, name, category, description, duration_hours, price, booking_required, best_time)
        VALUES (%(destination_id)s, %(name)s, %(category)s, %(description)s, %(duration_hours)s, %(price)s, %(booking_required)s, %(best_time)s)
        RETURNING id;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, activity_data)
                return cur.fetchone()[0]
        
    def create_tables(self):
        """Crée toutes les tables nécessaires"""
        
        queries = [
            # Table des destinations
            """
            CREATE TABLE IF NOT EXISTS destinations (
                id SERIAL PRIMARY KEY,
                country VARCHAR(100) NOT NULL,
                city VARCHAR(100) NOT NULL,
                description TEXT,
                best_time_to_visit VARCHAR(50),
                average_budget_per_day INTEGER,
                visa_required BOOLEAN DEFAULT FALSE,
                visa_info TEXT,
                vaccinations TEXT,
                safety_rating INTEGER CHECK (safety_rating >= 1 AND safety_rating <= 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Table des hébergements
            """
            CREATE TABLE IF NOT EXISTS accommodations (
                id SERIAL PRIMARY KEY,
                destination_id INTEGER REFERENCES destinations(id),
                name VARCHAR(200) NOT NULL,
                type VARCHAR(50) NOT NULL, -- hotel, hostel, airbnb, camping
                price_range VARCHAR(20), -- €, €€, €€€, €€€€
                average_price_per_night DECIMAL(10, 2),
                rating DECIMAL(3, 2),
                amenities TEXT[],
                address TEXT,
                booking_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Table des activités
            """
            CREATE TABLE IF NOT EXISTS activities (
                id SERIAL PRIMARY KEY,
                destination_id INTEGER REFERENCES destinations(id),
                name VARCHAR(200) NOT NULL,
                category VARCHAR(50), -- culture, nature, sport, food, nightlife
                description TEXT,
                duration_hours DECIMAL(4, 2),
                price DECIMAL(10, 2),
                booking_required BOOLEAN DEFAULT FALSE,
                best_time VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Table des utilisateurs (basique pour le moment)
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(200) UNIQUE NOT NULL,
                travel_style VARCHAR(50),
                preferred_budget_range VARCHAR(20),
                interests TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Table des conversations
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_id VARCHAR(100) NOT NULL,
                user_message TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                context JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Table des itinéraires sauvegardés
            """
            CREATE TABLE IF NOT EXISTS saved_itineraries (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title VARCHAR(200) NOT NULL,
                destination VARCHAR(200) NOT NULL,
                duration_days INTEGER,
                total_budget DECIMAL(10, 2),
                itinerary_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Index pour améliorer les performances
            """
            CREATE INDEX IF NOT EXISTS idx_destinations_country ON destinations(country);
            CREATE INDEX IF NOT EXISTS idx_destinations_city ON destinations(city);
            CREATE INDEX IF NOT EXISTS idx_activities_category ON activities(category);
            CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
            """
        ]
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for query in queries:
                    cur.execute(query)
                print("✅ Toutes les tables ont été créées avec succès !")
    
    def insert_destination(self, destination_data: Dict) -> int:
        """Insère une nouvelle destination"""
        
        query = """
        INSERT INTO destinations 
        (country, city, description, best_time_to_visit, average_budget_per_day, 
         visa_required, visa_info, vaccinations, safety_rating)
        VALUES (%(country)s, %(city)s, %(description)s, %(best_time_to_visit)s, 
                %(average_budget_per_day)s, %(visa_required)s, %(visa_info)s, 
                %(vaccinations)s, %(safety_rating)s)
        RETURNING id;
        """
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, destination_data)
                return cur.fetchone()[0]
    
    def insert_accommodation(self, accommodation_data: Dict) -> int:
        """Insère un nouvel hébergement"""
        
        query = """
        INSERT INTO accommodations 
        (destination_id, name, type, price_range, average_price_per_night, 
         rating, amenities, address, booking_url)
        VALUES (%(destination_id)s, %(name)s, %(type)s, %(price_range)s, 
                %(average_price_per_night)s, %(rating)s, %(amenities)s, 
                %(address)s, %(booking_url)s)
        RETURNING id;
        """
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, accommodation_data)
                return cur.fetchone()[0]
    
    def save_conversation(self, session_id: str, user_message: str, 
                         assistant_response: str, user_id: Optional[int] = None,
                         context: Optional[Dict] = None):
        """Sauvegarde une conversation"""
        
        query = """
        INSERT INTO conversations 
        (user_id, session_id, user_message, assistant_response, context)
        VALUES (%s, %s, %s, %s, %s::jsonb);
        """
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    user_id, 
                    session_id, 
                    user_message, 
                    assistant_response,
                    json.dumps(context) if context else None
                ))
    
    def search_destinations(self, query: str) -> List[Dict]:
        """Recherche des destinations"""
        
        sql = """
        SELECT * FROM destinations 
        WHERE country ILIKE %s OR city ILIKE %s
        ORDER BY country, city
        LIMIT 10;
        """
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                search_pattern = f"%{query}%"
                cur.execute(sql, (search_pattern, search_pattern))
                return cur.fetchall()
    
    def get_destination_details(self, destination_id: int) -> Dict:
        """Récupère tous les détails d'une destination"""
        
        # Récupérer la destination
        dest_query = "SELECT * FROM destinations WHERE id = %s;"
        
        # Récupérer les hébergements
        acc_query = """
        SELECT * FROM accommodations 
        WHERE destination_id = %s 
        ORDER BY rating DESC NULLS LAST;
        """
        
        # Récupérer les activités
        act_query = """
        SELECT * FROM activities 
        WHERE destination_id = %s 
        ORDER BY category, price;
        """
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Destination
                cur.execute(dest_query, (destination_id,))
                destination = cur.fetchone()
                
                if not destination:
                    return {}
                
                # Hébergements
                cur.execute(acc_query, (destination_id,))
                accommodations = cur.fetchall()
                
                # Activités
                cur.execute(act_query, (destination_id,))
                activities = cur.fetchall()
                
                return {
                    "destination": destination,
                    "accommodations": accommodations,
                    "activities": activities
                }
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Récupère l'historique d'une conversation"""
        
        query = """
        SELECT user_message, assistant_response, created_at 
        FROM conversations 
        WHERE session_id = %s 
        ORDER BY created_at DESC 
        LIMIT %s;
        """
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (session_id, limit))
                return cur.fetchall()[::-1]  # Inverser pour ordre chronologique

# Import json pour la sauvegarde des conversations
import json

def get_langchain_db() -> SQLDatabase:
    """
    Crée et retourne une connexion à la base de données compatible avec LangChain.
    Utilisée par l'agent IA pour interroger la BDD en langage naturel.
    """
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    # Important: Utiliser le nom du service Docker comme host, pas "localhost".
    db_host = os.getenv("POSTGRES_HOST", "db") 
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    # Format de l'URI pour SQLAlchemy, utilisé par LangChain
    db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Création de l'objet SQLDatabase que l'agent LangChain pourra utiliser
    return SQLDatabase.from_uri(db_uri)
