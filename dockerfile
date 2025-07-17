# Étape 1: Choisir une image de base légère
# On part d'une image Python officielle et optimisée en taille (-slim).
FROM python:3.10-slim

# Étape 2: Définir le répertoire de travail dans le conteneur
# Toutes les commandes suivantes s'exécuteront depuis ce dossier.
WORKDIR /app

# Étape 3: Copier et installer les dépendances (OPTIMISATION)
# On copie d'abord SEULEMENT le fichier des dépendances.
# Docker met cette étape en cache. Si vous ne changez que le code,
# il ne réinstallera pas tout, ce qui accélère les builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4: Copier le reste du code de l'application
# Maintenant que les dépendances sont installées, on copie tout le reste.
COPY . .

# Étape 5: Exposer le port de Streamlit
# On indique que l'application va écouter sur le port 8501.
EXPOSE 8501

# Étape 6: Définir la commande pour lancer l'application
# C'est la commande qui s'exécutera au démarrage du conteneur.
# --server.address=0.0.0.0 est nécessaire pour rendre l'app accessible
# depuis l'extérieur du conteneur.
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]