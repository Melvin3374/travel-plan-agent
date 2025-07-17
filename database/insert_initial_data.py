"""
Script pour insérer des données initiales dans la base de données
Pour avoir un jeu de données de départ
"""

from postgres_db import DatabaseManager

def insert_initial_data():
    """Insère un jeu de données initial pour tester l'application"""
    
    db = DatabaseManager()
    
    # D'abord, créer les tables
    print("📊 Création des tables...")
    db.create_tables()
    
    # Données de destinations
    destinations = [
        {
            "country": "France",
            "city": "Paris",
            "description": "La ville lumière, capitale de la France, connue pour sa Tour Eiffel, ses musées et sa gastronomie",
            "best_time_to_visit": "Avril-Juin, Septembre-Octobre",
            "average_budget_per_day": 100,
            "visa_required": False,
            "visa_info": "Pas de visa requis pour l'UE, 90 jours max pour autres nationalités",
            "vaccinations": "Aucune vaccination obligatoire",
            "safety_rating": 4
        },
        {
            "country": "Thaïlande",
            "city": "Bangkok",
            "description": "Capitale vibrante de la Thaïlande, mélange de tradition et modernité",
            "best_time_to_visit": "Novembre-Mars",
            "average_budget_per_day": 40,
            "visa_required": True,
            "visa_info": "Visa à l'arrivée 30 jours ou e-visa 60 jours",
            "vaccinations": "Hépatites A/B recommandées, paludisme selon régions",
            "safety_rating": 4
        },
        {
            "country": "Japon",
            "city": "Tokyo",
            "description": "Mégapole futuriste où tradition et modernité se côtoient harmonieusement",
            "best_time_to_visit": "Mars-Mai (cerisiers), Octobre-Novembre",
            "average_budget_per_day": 80,
            "visa_required": False,
            "visa_info": "Exemption de visa 90 jours pour tourisme",
            "vaccinations": "Aucune vaccination obligatoire",
            "safety_rating": 5
        },
        {
            "country": "Pérou",
            "city": "Cusco",
            "description": "Ancienne capitale de l'empire Inca, porte d'entrée vers le Machu Picchu",
            "best_time_to_visit": "Mai-Septembre (saison sèche)",
            "average_budget_per_day": 35,
            "visa_required": False,
            "visa_info": "Pas de visa pour séjours < 183 jours",
            "vaccinations": "Fièvre jaune recommandée pour l'Amazonie",
            "safety_rating": 3
        },
        {
            "country": "Islande",
            "city": "Reykjavik",
            "description": "Capitale nordique, base idéale pour explorer les merveilles naturelles islandaises",
            "best_time_to_visit": "Juin-Août (été), Septembre-Mars (aurores)",
            "average_budget_per_day": 120,
            "visa_required": False,
            "visa_info": "Espace Schengen, 90 jours max",
            "vaccinations": "Aucune vaccination obligatoire",
            "safety_rating": 5
        }
    ]
    
    # Insérer les destinations et garder les IDs
    destination_ids = {}
    print("\n🌍 Insertion des destinations...")
    
    for dest in destinations:
        try:
            dest_id = db.insert_destination(dest)
            destination_ids[f"{dest['country']}_{dest['city']}"] = dest_id
            print(f"✅ {dest['city']}, {dest['country']} ajouté")
        except Exception as e:
            print(f"❌ Erreur pour {dest['city']}: {e}")
    
    # Données d'hébergements
    accommodations = [
        # Paris
        {
            "destination_id": destination_ids.get("France_Paris"),
            "name": "Hôtel des Grands Boulevards",
            "type": "hotel",
            "price_range": "€€€",
            "average_price_per_night": 180,
            "rating": 4.5,
            "amenities": ["wifi", "restaurant", "bar", "room_service"],
            "address": "17 Boulevard Poissonnière, 75002 Paris",
            "booking_url": "https://booking.com"
        },
        {
            "destination_id": destination_ids.get("France_Paris"),
            "name": "Le Village Montmartre",
            "type": "hostel",
            "price_range": "€",
            "average_price_per_night": 35,
            "rating": 4.2,
            "amenities": ["wifi", "kitchen", "lounge", "lockers"],
            "address": "20 Rue d'Orsel, 75018 Paris",
            "booking_url": "https://hostelworld.com"
        },
        
        # Bangkok
        {
            "destination_id": destination_ids.get("Thaïlande_Bangkok"),
            "name": "Mandarin Oriental Bangkok",
            "type": "hotel",
            "price_range": "€€€€",
            "average_price_per_night": 300,
            "rating": 4.8,
            "amenities": ["wifi", "pool", "spa", "restaurant", "gym"],
            "address": "48 Oriental Avenue, Bangkok",
            "booking_url": "https://booking.com"
        },
        {
            "destination_id": destination_ids.get("Thaïlande_Bangkok"),
            "name": "Lub d Bangkok Siam",
            "type": "hostel",
            "price_range": "€",
            "average_price_per_night": 15,
            "rating": 4.3,
            "amenities": ["wifi", "ac", "lounge", "kitchen"],
            "address": "925/9 Rama I Rd, Bangkok",
            "booking_url": "https://hostelworld.com"
        },
        
        # Tokyo
        {
            "destination_id": destination_ids.get("Japon_Tokyo"),
            "name": "Park Hyatt Tokyo",
            "type": "hotel",
            "price_range": "€€€€",
            "average_price_per_night": 400,
            "rating": 4.7,
            "amenities": ["wifi", "pool", "spa", "restaurant", "bar", "gym"],
            "address": "3-7-1-2 Nishi Shinjuku, Tokyo",
            "booking_url": "https://booking.com"
        },
        {
            "destination_id": destination_ids.get("Japon_Tokyo"),
            "name": "K's House Tokyo",
            "type": "hostel",
            "price_range": "€",
            "average_price_per_night": 25,
            "rating": 4.4,
            "amenities": ["wifi", "kitchen", "lounge", "laundry"],
            "address": "3-20-10 Kuramae, Taito-ku, Tokyo",
            "booking_url": "https://kshouse.jp"
        }
    ]
    
    # Insérer les hébergements
    print("\n🏨 Insertion des hébergements...")
    
    for acc in accommodations:
        if acc["destination_id"]:  # Vérifier que la destination existe
            try:
                db.insert_accommodation(acc)
                print(f"✅ {acc['name']} ajouté")
            except Exception as e:
                print(f"❌ Erreur pour {acc['name']}: {e}")
    
    # Données d'activités
    activities = [
        # Paris
        {
            "destination_id": destination_ids.get("France_Paris"),
            "name": "Visite de la Tour Eiffel",
            "category": "culture",
            "description": "Montée au sommet du monument le plus emblématique de Paris",
            "duration_hours": 2.5,
            "price": 26.10,
            "booking_required": True,
            "best_time": "Matin ou fin d'après-midi"
        },
        {
            "destination_id": destination_ids.get("France_Paris"),
            "name": "Croisière sur la Seine",
            "category": "culture",
            "description": "Découverte des monuments parisiens depuis la Seine",
            "duration_hours": 1.5,
            "price": 15,
            "booking_required": False,
            "best_time": "Coucher de soleil"
        },
        
        # Bangkok
        {
            "destination_id": destination_ids.get("Thaïlande_Bangkok"),
            "name": "Visite du Grand Palais",
            "category": "culture",
            "description": "Complexe de temples et palais royaux éblouissants",
            "duration_hours": 3,
            "price": 15,
            "booking_required": False,
            "best_time": "Matin tôt"
        },
        {
            "destination_id": destination_ids.get("Thaïlande_Bangkok"),
            "name": "Street Food Tour",
            "category": "food",
            "description": "Découverte de la cuisine de rue thaïlandaise",
            "duration_hours": 3,
            "price": 25,
            "booking_required": True,
            "best_time": "Soir"
        },
        
        # Tokyo
        {
            "destination_id": destination_ids.get("Japon_Tokyo"),
            "name": "Visite du temple Senso-ji",
            "category": "culture",
            "description": "Plus ancien temple bouddhiste de Tokyo",
            "duration_hours": 2,
            "price": 0,
            "booking_required": False,
            "best_time": "Matin"
        },
        {
            "destination_id": destination_ids.get("Japon_Tokyo"),
            "name": "Experience Onsen",
            "category": "nature",
            "description": "Bains thermaux traditionnels japonais",
            "duration_hours": 2,
            "price": 20,
            "booking_required": False,
            "best_time": "Fin d'après-midi"
        }
    ]
    
    # Insérer les activités
    print("\n🎯 Insertion des activités...")
    
    for activity in activities:
        if activity["destination_id"]:
            try:
                # On utilise la nouvelle méthode propre !
                db.insert_activity(activity)
                print(f"✅ {activity['name']} ajouté")
            except Exception as e:
                print(f"❌ Erreur pour {activity['name']}: {e}")
    
    print("\n✨ Insertion des données initiales terminée !")

if __name__ == "__main__":
    insert_initial_data()