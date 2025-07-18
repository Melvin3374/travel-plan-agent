# Fichier : database/postgres_db.py (Version finale et unifiée)

import os
import json
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from typing import Dict, List, Optional

load_dotenv()

def get_db_connection():
    """
    Fonction utilitaire pour obtenir une connexion à la base de données
    en utilisant la variable d'environnement DATABASE_URL.
    """
    db_uri = os.getenv("DATABASE_URL")
    if not db_uri:
        raise ValueError("DATABASE_URL n'est pas définie dans le fichier .env")
    if "?sslmode" not in db_uri:
        db_uri += "?sslmode=require"
    return psycopg2.connect(db_uri)

def get_info_for_city(city_name: str) -> str:
    """
    Récupère toutes les informations pour une ville donnée.
    """
    destination_id = None
    details = {}

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # 1. Trouver l'ID de la destination
                cur.execute("SELECT id FROM destinations WHERE city ILIKE %s", (city_name,))
                result = cur.fetchone()
                if result:
                    destination_id = result['id']
                else:
                    return f"Je n'ai trouvé aucune information pour la ville de {city_name} dans la base de données."

                # 2. Récupérer tous les détails
                cur.execute("SELECT * FROM destinations WHERE id = %s;", (destination_id,))
                details['destination'] = cur.fetchone()
                cur.execute("SELECT * FROM accommodations WHERE destination_id = %s;", (destination_id,))
                details['accommodations'] = cur.fetchall()
                cur.execute("SELECT * FROM activities WHERE destination_id = %s;", (destination_id,))
                details['activities'] = cur.fetchall()

    except Exception as e:
        print(f"Erreur lors de la connexion ou de la requête à la base de données : {e}")
        return "Erreur lors de la récupération des informations de la base de données."

    # 3. Formater le résultat pour l'IA
    output = f"Voici les informations trouvées pour {city_name}:\n"
    if details.get('destination'):
        output += f"- Description: {details['destination'].get('description', 'N/A')}\n"
        output += f"- Vaccins: {details['destination'].get('vaccinations', 'N/A')}\n"
    
    if details.get('accommodations'):
        output += "\nHébergements:\n"
        for acc in details['accommodations']:
            output += f"  - {acc.get('name')} ({acc.get('type')}), Prix: {acc.get('average_price_per_night')}€, Note: {acc.get('rating')}\n"
            
    if details.get('activities'):
        output += "\nActivités:\n"
        for act in details['activities']:
            output += f"  - {act.get('name')} ({act.get('category')})\n"
            
    return output

# La fonction get_langchain_db est conservée pour la compatibilité future
# mais n'est plus utilisée par l'agent actuel.
def get_langchain_db() -> SQLDatabase:
    db_uri = os.getenv("DATABASE_URL")
    if not db_uri:
        raise ValueError("DATABASE_URL n'est pas définie !")
    if "?sslmode" not in db_uri:
        db_uri += "?sslmode=require"
    if "postgresql+psycopg2://" not in db_uri:
        db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://", 1)
    return SQLDatabase.from_uri(db_uri)