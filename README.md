# 🧳 Assistant IA de Planification de Voyage

Un assistant conversationnel intelligent qui aide à planifier des voyages personnalisés en utilisant Gemini AI et LangChain.

## 🎯 Fonctionnalités

- 💬 **Chatbot conversationnel** : Interface naturelle style ChatGPT
- 🧠 **Mémoire contextuelle** : Mémorise vos préférences et habitudes
- 🔍 **Recherche intelligente** : Base de données interne + recherche web
- 📋 **Plans complets** : Itinéraires, hébergements, activités, infos pratiques
- 🔐 **Sécurisé** : RGPD compliant, données chiffrées

## 🛠️ Technologies

- **IA/LLM** : Google Gemini Pro
- **Framework** : LangChain
- **Frontend** : Streamlit
- **Backend** : Python 3.9+
- **Base de données** : PostgreSQL
- **Containerisation** : Docker
- **Authentification** : Firebase (à venir)

## 🚀 Installation rapide

### Prérequis

- Python 3.9+
- Docker Desktop
- Clé API Gemini (obtenir sur [Google AI Studio](https://makersuite.google.com/app/apikey))

### Étapes

1. **Cloner le projet**
```bash
git clone [votre-repo]
cd PROJET_FIL_ROUGE
```

2. **Créer l'environnement virtuel**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé Gemini
```

5. **Lancer l'application**
```bash
python start.py
```

L'application sera accessible sur http://localhost:8501

## 📁 Structure du projet

```
PROJET_FIL_ROUGE/
├── app/                    # Application Streamlit
│   ├── main.py            # Point d'entrée principal
│   └── requirements.txt   # Dépendances Python
├── chatbot/               # Logique du chatbot
│   ├── chatbot_core.py    # Agent LangChain/Gemini
│   └── chat_cli.py        # Interface CLI (tests)
├── database/              # Gestion base de données
│   ├── postgres_db.py     # Manager PostgreSQL
│   ├── insert_initial_data.py  # Données de démarrage
│   └── migrate_table.py   # Migrations
├── agents/                # Agents spécialisés (futur)
├── utils/                 # Utilitaires
├── docker-compose.yml     # Configuration Docker
├── Dockerfile            # Image Docker app
├── start.py              # Script de démarrage
└── README.md             # Ce fichier
```

## 💻 Utilisation

### Interface principale

1. **Définir vos préférences** dans la barre latérale :
   - Style de voyage (backpacker, confort, luxe)
   - Budget journalier
   - Centres d'intérêt

2. **Converser avec l'assistant** :
   - "Je veux partir 2 semaines au Japon"
   - "Trouve-moi un itinéraire pour visiter la Thaïlande"
   - "Quels vaccins pour le Pérou ?"

3. **Obtenir un plan détaillé** avec :
   - Itinéraire jour par jour
   - Hébergements recommandés
   - Activités et visites
   - Infos pratiques (visa, vaccins)
   - Budget estimé

### Commandes utiles

```bash
# Démarrer uniquement PostgreSQL
docker-compose up -d postgres

# Voir les logs
docker-compose logs -f

# Accéder à PgAdmin
# http://localhost:5050
# Email: admin@travel.com
# Password: admin

# Arrêter tous les services
docker-compose down
```

## 🔧 Configuration avancée

### Variables d'environnement

```bash
# API Keys
GEMINI_API_KEY=your_key_here

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=travel_assistant
POSTGRES_USER=travel_user
POSTGRES_PASSWORD=secure_password

# Application
DEBUG_MODE=True
APP_SECRET_KEY=your_secret_key
```

### Ajouter des destinations

Utiliser le script `database/insert_initial_data.py` ou directement via PgAdmin.

## 🧪 Tests

```bash
# Tests unitaires
pytest tests/

# Linter
pylint app/ chatbot/ database/

# Formatage
black .
```

## 🔒 Sécurité

- ✅ Variables d'environnement pour les secrets
- ✅ Validation des entrées utilisateur
- ✅ Connexions DB sécurisées
- ✅ Rate limiting (à venir)
- ✅ Chiffrement des données sensibles (à venir)

## 📝 Roadmap

- [x] MVP avec chatbot fonctionnel
- [x] Base de données PostgreSQL
- [x] Interface Streamlit
- [ ] Authentification utilisateur
- [ ] Recherche web en temps réel
- [ ] Export PDF des itinéraires
- [ ] Version mobile
- [ ] API REST
- [ ] Intégrations partenaires (Booking, etc.)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Projet réalisé dans le cadre d'une alternance Data & IA Engineering.

---

**Note** : Ce projet est en développement actif. Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue !